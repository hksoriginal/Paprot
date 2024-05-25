from abc import ABC, abstractmethod


class ValidateResultsInteractorInterface(ABC):

    @abstractmethod
    def validate_commonality(self, input_text: str, search_result: str) -> bool:
        pass

    @abstractmethod
    def validate_results(self, search_result: str, input_text: str) -> bool:
        pass
