from abc import ABC, abstractmethod


class CreateAndStoreEmbeddingsPresenterInterface(ABC):
    @abstractmethod
    def clean_directory(self, directory_path: str):
        pass

    @abstractmethod
    def create_and_store_embeddings_from_policies(self,
                                                  folder_path: str) -> str:
        pass
