from abc import ABC, abstractmethod


class HuggingfaceEmbeddingsInteractorInterface(ABC):
    @abstractmethod
    def get_embeddings_object(self):
        pass
