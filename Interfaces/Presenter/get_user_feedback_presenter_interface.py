from abc import ABC, abstractmethod

from DTOs.Databases.user_feedback_dtos import UserFeedbackDTO


class UserFeedbackPresenterInterface(ABC):
    @abstractmethod
    def store_user_feedback(self, user_feedback_dto: UserFeedbackDTO):
        pass

    @abstractmethod
    def record_user_feedback_in_excel_sheet(self,
                                            user_feedback_dto: UserFeedbackDTO):
        pass
