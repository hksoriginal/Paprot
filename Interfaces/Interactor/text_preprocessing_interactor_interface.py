from abc import ABC, abstractmethod
from typing import List


class TextProcessingInteractorInterface(ABC):
    @abstractmethod
    def remove_consecutive_repeating_words(self, text: str) -> str:
        pass

    @abstractmethod
    def clean_text(self, text: str) -> str:
        pass

    @abstractmethod
    def handling_numerical_fractions(self, text: str) -> str:
        pass

    @abstractmethod
    def add_source_in_response_text(self,
                                    response_text: str,
                                    source_docs: List[str]) -> str:
        pass

    @abstractmethod
    def profanity_check(self, text: str) -> bool:
        pass

    @abstractmethod
    def text_post_processing(self, text: str, source_docs: List[str]) -> str:
        pass

    @abstractmethod
    def create_compound_words(self, text: str) -> str:
        pass

    @abstractmethod
    def special_token_remover(self, text: str) -> str:
        pass
