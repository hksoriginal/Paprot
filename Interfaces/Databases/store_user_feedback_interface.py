from abc import ABC, abstractmethod

from DTOs.Databases.user_feedback_dtos import UserFeedbackDTO


class StoreUserFeedbackInterface(ABC):
    @abstractmethod
    def store_user_feedback(self, user_feedback_dto: UserFeedbackDTO) -> str:
        pass
