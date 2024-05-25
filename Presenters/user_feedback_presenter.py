from DTOs.Databases.user_feedback_dtos import UserFeedbackDTO
from Databases.store_user_feedback import StoreUserFeedback
from Interactors.record_user_feedback_interactor import \
    RecordUserFeedBackInteractor

from Interfaces.Presenter.get_user_feedback_presenter_interface import \
    UserFeedbackPresenterInterface


class UserFeedbackPresenter(UserFeedbackPresenterInterface):
    def store_user_feedback(self, user_feedback_dto: UserFeedbackDTO):
        """
            Stores user feedback in a database using the StoreUserFeedback class.

            Args:
                user_feedback_dto (UserFeedbackDTO): A Data Transfer Object containing the user's feedback.

            Returns:
                The response from the store_user_feedback method of the StoreUserFeedback class.
                    This response type may vary depending on the implementation of StoreUserFeedback.
            """
        store_user_feedback_database = StoreUserFeedback()
        response_from_db = store_user_feedback_database.store_user_feedback(
            user_feedback_dto=user_feedback_dto)
        return response_from_db

    def record_user_feedback_in_excel_sheet(self,
                                            user_feedback_dto: UserFeedbackDTO):
        """
            Records user feedback in an Excel sheet using the RecordUserFeedbackInteractor.

            Args:
                user_feedback_dto (UserFeedbackDTO): A Data Transfer Object containing the user's feedback.

            Returns:
                The result of the record_user_feedback method from the RecordUserFeedbackInteractor.

            Raises:
                (Optional) Exceptions that may occur during the recording process.
            """
        record_user_feedback_interactor = RecordUserFeedBackInteractor()
        return record_user_feedback_interactor.record_user_feedback(
            user_feedback_dto=user_feedback_dto
        )
