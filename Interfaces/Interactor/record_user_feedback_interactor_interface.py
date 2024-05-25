from DTOs.Databases.user_feedback_dtos import UserFeedbackDTO
from abc import ABC, abstractmethod


class RecordUserFeedBackInteractorInterface(ABC):
    @abstractmethod
    def record_user_feedback(self, user_feedback_dto: UserFeedbackDTO) -> str:
        pass
