from abc import ABC, abstractmethod
from typing import List, Any
from langchain.docstore.document import Document


class GetPolicyDocumentsChunksInteractorInterface(ABC):
    @abstractmethod
    def remove_special_characters(self, text: str) -> str:
        pass

    @abstractmethod
    def split_text_into_chunks(self, file_content: str, chunk_size: int):
        pass

    @abstractmethod
    def _get_faqs_chunks(self, file_path: str) -> List[Any]:
        pass

    @abstractmethod
    def get_pdf_document_objects(self, file_path: str) -> Document:
        pass

    @abstractmethod
    def _get_pdf_documents(self, pdf_folder_path: str) -> List[Any]:
        pass

    @abstractmethod
    def _get_documents_chunks(self, documents: List[Any],
                              chunk_size=1000,
                              chunk_overlap=100) -> List[Any]:
        pass

    @abstractmethod
    def get_policy_documents_chunks(self, folder_path: str) -> List[Any]:
        pass
