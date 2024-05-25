import os

from Interactors.get_documents_chunks_interactor import \
    GetdocumentDocumentsChunksInteractor
from Interactors.store_vector_embeddings_interactor import \
    StoreVectorEmbeddingsInteractor
from Interfaces.Presenter. \
    create_and_store_embeddings_presenter_interface import \
    CreateAndStoreEmbeddingsPresenterInterface
import shutil
import warnings


class CreateAndStoreEmbeddingsPresenter(
    CreateAndStoreEmbeddingsPresenterInterface):

    def __init__(self):
        self.directory_path = os.path.abspath(
            './../Persist_Directory/document_cosine')
        self.clean_directory(directory_path=self.directory_path)

    def clean_directory(self, directory_path: str):
        """
        Clean up a directory by deleting all its contents.

        Args:
            directory_path (str): The path to the directory to be cleaned.

        Raises:
            OSError: If the directory could not be removed.
        """
        try:
            shutil.rmtree(directory_path)
            warnings.warn(
                f"Directory '{directory_path}' "
                f"and its contents deleted.")
        except Exception as e:
            print(f"Error deleting directory '{directory_path}': {e}")

    def create_and_store_embeddings_from_policies(self,
                                                  folder_path: str) -> str:
        """
        Create and store embeddings from documents stored in the specified folder.

        Args:
            folder_path (str): The path to the folder containing document documents.

        Returns:
            str: A message indicating the status of the embedding storage process.
        """
        get_documents_chunks = GetdocumentDocumentsChunksInteractor()
        store_vector_embeddings = StoreVectorEmbeddingsInteractor()

        documents_chunks = get_documents_chunks.get_document_documents_chunks(
            folder_path=folder_path
        )

        store_embeddings = store_vector_embeddings.store_vector_embeddings(
            chunked_documents=documents_chunks
        )

        print("document Embeddings stored")

        return store_embeddings
