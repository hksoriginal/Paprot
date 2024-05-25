from abc import ABC, abstractmethod
from typing import List
from langchain import PromptTemplate


class PromptTemplateInteractorInterface(ABC):
    @abstractmethod
    def get_prompt_template(self, prompt_template_text: str,
                            input_variables: List[str]):
        pass
