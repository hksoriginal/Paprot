from typing import List, Any
from abc import ABC, abstractmethod


class VectorStoresInteractorInterface(ABC):
    @abstractmethod
    def create_vector_stores(self, file_path: str, documents: List[str],
                             embeddings: Any):
        pass

    @abstractmethod
    def load_vector_stores(self, file_path: str, embedding_function: Any):
        pass
