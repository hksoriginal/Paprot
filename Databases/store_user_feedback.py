import sqlite3

from DTOs.Databases.user_feedback_dtos import UserFeedbackDTO
from Interfaces.Databases.store_user_feedback_interface import \
    StoreUserFeedbackInterface


class StoreUserFeedback(StoreUserFeedbackInterface):
    def store_user_feedback(self, user_feedback_dto: UserFeedbackDTO) -> str:
        """
               Store user feedback in a SQLite database.

               Parameters:
               - user_feedback_dto (UserFeedbackDTO): An object containing user
               feedback details.

               Returns:
               - str: A message indicating the status of the database update.
               """

        try:
            time = user_feedback_dto.time
            date = user_feedback_dto.date
            user_email = user_feedback_dto.user_email
            user_input = user_feedback_dto.user_input
            response_received = user_feedback_dto.response_received
            feedback = user_feedback_dto.feedback

            conn = sqlite3.connect('./DB_files/hrb_user_feedback.db')
            cursor = conn.cursor()

            cursor.execute('''
                       CREATE TABLE IF NOT EXISTS user_feedback (
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           user_email TEXT NOT NULL,
                           feedback_date DATE,
                           feedback_time TIME,
                           user_input TEXT NOT NULL,
                           response_received TEXT NOT NULL,
                           feedback TEXT NOT NULL
                       );
                   ''')

            cursor.execute(
                '''INSERT INTO user_feedback (user_email, 
                feedback_date,feedback_time,user_input, 
                response_received, feedback ) VALUES (?,?,?,?,?,?)''',
                (user_email, date, time, user_input,
                 response_received, feedback))

            conn.commit()
            conn.close()

            return "Database Updated!"

        except Exception as e:
            return f"Error updating database: {str(e)}"
