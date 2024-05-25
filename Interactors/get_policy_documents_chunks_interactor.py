import os
from typing import List, Any, Tuple, Iterable
from langchain.text_splitter import RecursiveCharacterTextSplitter
from PyPDF2 import PdfReader
import re
from tqdm import tqdm
from Constants.chunking_constants import CHUNK_SIZE, CHUNK_OVERLAP
from Interfaces.Interactor. \
    get_policy_documents_chunks_Interactor_interface import \
    GetPolicyDocumentsChunksInteractorInterface
from langchain.docstore.document import Document
from rich.console import Console

console = Console()


class GetPolicyDocumentsChunksInteractor(
    GetPolicyDocumentsChunksInteractorInterface):

    def remove_special_characters(self, text: str) -> str:
        """
        Removes special characters like '\n' (newline) from a string.

        Args:
            text (str): The input string.

        Returns:
            str: The string after removing special characters.
        """
        text = " ".join(text.split())
        cleaned_text = re.sub(r'\n', '', text)
        return cleaned_text

    def split_text_into_chunks(
            self, file_content: str, chunk_size: int,
            overlap: int = 0) -> list[str]:
        """
        Splits a text string into chunks of a specified size, preserving word boundaries
        and introducing optional overlap between chunks.

        Args:
            file_content (str): The text string to be split.
            chunk_size (int): The desired maximum size of each chunk in words (excluding overlap).
            overlap (int, optional): The number of words to overlap between chunks. Defaults to 0.

        Returns:
            list[str]: A list of text chunks, each containing at most `chunk_size` words.
        """
        if overlap < 0:
            raise ValueError("Overlap cannot be negative")

        words = file_content.split()
        chunks = []
        for i in range(0, len(words), chunk_size - overlap):
            end_index = min(i + chunk_size, len(words))
            chunk = " ".join(words[i:end_index])
            chunks.append(chunk)
        return chunks

    def get_pdf_document_objects(self, file_path: str) -> Document:
        pdf_text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PdfReader(file)
            for page_num in tqdm(range(len(pdf_reader.pages)),
                                 desc=f"Processing Policy document :"
                                      f" {file_path}", colour='GREEN'):
                page = pdf_reader.pages[page_num]
                pdf_text += page.extract_text()
                pdf_text = " ".join(pdf_text.split())
        return Document(page_content=pdf_text,
                        metadata={"source": file_path})

    def _get_faqs_chunks(self, file_path: str) -> List[Any]:
        """
            Extracts FAQ chunks from a PDF file, splitting them into smaller chunks
            if they exceed a specified size.

            Args:
                file_path (str): The path to the PDF file containing FAQs.

            Returns:
                List[Document]: A list of Document objects, each representing a FAQ chunk
                    with its content and source file metadata.
        """
        pdf_text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PdfReader(file)
            for page_num in tqdm(range(len(pdf_reader.pages)),
                                 desc=f"Processing FAQ document : "
                                      f"{file_path}",
                                 colour='CYAN'):
                page = pdf_reader.pages[page_num]
                pdf_text += page.extract_text()

        pattern = r'\d+\.\s*(.*?)\n(.*?)(?=\d+\.|$)'
        matches = re.findall(pattern, pdf_text, re.DOTALL)
        faq_chunks_texts = [''.join(match) for match in matches]

        filtered_faq_chunks = []
        for chunk in faq_chunks_texts:
            if len(chunk) >= CHUNK_SIZE:
                filtered_faq_chunks.extend(
                    self.split_text_into_chunks(file_content=chunk,
                                                overlap=CHUNK_OVERLAP,
                                                chunk_size=CHUNK_SIZE//2)
                )
            else:
                filtered_faq_chunks.append(chunk)

        document_list = [
            Document(page_content=self.remove_special_characters(chunk),
                     metadata={"source": file_path})
            for chunk in filtered_faq_chunks
        ]
        return document_list

    def _get_pdf_documents(self, pdf_folder_path) -> \
            Tuple[List[Any], List[Any]]:
        """
            Loads PDF documents and extracts FAQ chunks from designated files within a folder.

            Args:
                pdf_folder_path (str): The path to the folder containing PDF documents.

            Returns:
                Tuple[List[UnstructuredPDFLoader], List[Document]]: A tuple containing two lists:
                    - The first list contains UnstructuredPDFLoader objects representing loaded PDF documents.
                    - The second list contains Document objects representing extracted FAQ chunks.

            Raises:
                OSError: If an error occurs while accessing the folder or its contents.
            """
        pdf_documents = []
        faq_chunks = []
        try:
            for root, dirs, files in os.walk(pdf_folder_path):
                for file_name in files:
                    file_path = os.path.join(root, file_name)
                    if file_name.endswith('.pdf'):
                        if 'FAQ' in file_name:
                            faq_chunks.extend(self._get_faqs_chunks(file_path))
                        pdf_documents.append(self.get_pdf_document_objects(
                            file_path=file_path))
                    else:
                        print(f"Skipping non-PDF file: {file_name}")
        except OSError as e:
            print(f"Error while loading PDF documents: {e}")
        return pdf_documents, faq_chunks

    def _get_documents_chunks(self, documents: List[Document],
                              chunk_size=CHUNK_SIZE,
                              chunk_overlap=CHUNK_OVERLAP) -> List[Document]:

        """
            Splits documents into overlapping character-based chunks.

            Args:
                documents (List[Iterable[Document]]): A list of documents to be split.
                chunk_size (int, optional): The desired maximum chunk size in characters. Defaults to CHUNK_SIZE.
                chunk_overlap (int, optional): The amount of character overlap between consecutive chunks. Defaults to CHUNK_OVERLAP.

            Returns:
                List[Any]: A list of chunked documents, each containing a portion of the original text.

            Raises:
                Exception: If an error occurs during text splitting.
            """
        try:
            console.print('\x1b[38;2;255;165;0m' +
                          "Chunking Documents...." +
                          '\x1b[0m')
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                length_function=len,
                is_separator_regex=False
            )
            return text_splitter.split_documents(documents=documents)
        except Exception as e:
            print(f"Error while splitting documents into chunks: {e}")

    def get_policy_documents_chunks(self, folder_path: str) -> List[Any]:
        """
            Retrieves and processes policy documents and FAQ chunks from a specified folder.

            Args:
                folder_path (str): The path to the folder containing policy documents (PDFs) and FAQs (separate files).

            Returns:
                List[Any]: A list containing chunked policy documents and FAQ chunks.

            Raises:
                Exception: If errors occur during file access, PDF processing, text chunking, or FAQ extraction.
            """
        try:
            documents, faq_chunks = self._get_pdf_documents(
                pdf_folder_path=folder_path)
            chunked_documents = self._get_documents_chunks(documents=documents)
            chunked_documents.extend(faq_chunks)
            return chunked_documents
        except Exception as e:
            print(f"Error while getting policy documents chunks: {e}")
