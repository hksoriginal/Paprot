from abc import abstractmethod, ABC
from typing import Any


class RetrievalQAInteractorInterface(ABC):
    @abstractmethod
    def get_retrievalqa(self, retriever: Any,
                        prompt_template: Any,
                        llm: Any):
        pass
