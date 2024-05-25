from abc import ABC, abstractmethod


class LoadLLMInteractorInterface(ABC):
    @abstractmethod
    def load_llm_model(self, local_llm_path: str):
        pass
