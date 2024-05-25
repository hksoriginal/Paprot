from typing import List, Any

from langchain_community.vectorstores import Chroma, FAISS

from Interfaces.Interactor.vector_stores_interactor_interface import \
    VectorStoresInteractorInterface


class VectorStoresInteractor(VectorStoresInteractorInterface):
    def create_vector_stores(self, file_path: str, documents: List[str],
                             embeddings: Any):
        """
            Creates a Chroma vector store from a list of documents and their corresponding embeddings.

            Args:
                file_path (str): The path to persist the vector store.
                documents (List[str]): A list of documents to be stored.
                embeddings (List[List[float]]): A list of embeddings, where each element is a list of floats
                    representing the embedding vector for a corresponding document.

            Returns:
                Chroma: The created Chroma vector store instance.
        """
        return Chroma.from_documents(
            documents=documents,
            embeddings=embeddings,
            collection_metadata={"hnsw:space": "cosine"},
            persist_directory=file_path
        )

    def load_vector_stores(self, file_path: str, embedding_function: Any):
        """
            Loads a Chroma vector store from a persisted directory.

            Args:
                file_path (str): The path to the previously persisted vector store directory.
                embedding_function (Callable[[str], Any]): A function that takes a text string
                    and returns its embedding representation.

            Returns:
                Chroma: The loaded Chroma vector store instance.

        """
        return Chroma(persist_directory=file_path,
                      embedding_function=embedding_function)
