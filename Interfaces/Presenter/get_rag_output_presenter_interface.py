from abc import ABC, abstractmethod
from typing import Optional, Tuple, List


class GetRAGOutputPresenterInterface(ABC):
    @abstractmethod
    def get_output(self, input_query: str) -> Optional[Tuple[str, List[str]]]:
        pass
