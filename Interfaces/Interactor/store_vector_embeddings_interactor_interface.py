from abc import ABC, abstractmethod
from typing import List, Any


class StoreVectorEmbeddingsInteractorInterface(ABC):

    @abstractmethod
    def store_vector_embeddings(self, chunked_documents: List[Any]) -> str:
        pass
