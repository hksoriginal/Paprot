from typing import List, Any
import shutil
from langchain_community.vectorstores.chroma import Chroma

from Interactors.get_embedding_using_huggingface import \
    HuggingfaceEmbeddingsInteractor
from Interfaces.Interactor.store_vector_embeddings_interactor_interface import \
    StoreVectorEmbeddingsInteractorInterface


class StoreVectorEmbeddingsInteractor(StoreVectorEmbeddingsInteractorInterface):

    def store_vector_embeddings(self, chunked_documents: List[Any]) -> str:
        """
            Stores vector embeddings for a collection of documents using a Chroma vector store.

            Args:
                chunked_documents (List[Any]): A list of documents to be processed and embedded.

            Returns:
                str: A message indicating success or failure and the storage location.

            Raises:
                (Optional) Exceptions that may occur during embedding generation, vector store creation,
                    or persisting to disk.
            """
        try:
            hugging_face_embeddings = HuggingfaceEmbeddingsInteractor()

            embeddings = hugging_face_embeddings.get_embeddings_object()

            persistent_directory = './../Persist_Directory/policy_cosine'

            vector_store = Chroma.from_documents(
                documents=chunked_documents,
                embedding=embeddings,
                collection_metadata={"hnsw:space": "cosine"},
                persist_directory=persistent_directory
            )
            return f"Embeddings stored successfully at {persistent_directory}"
        except Exception as e:
            return f"Error occurred while storing embeddings: {str(e)}"
