from typing import *
import sqlite3


class UserFeedback:
    def store_user_feedback(self, user_feedback: Dict[str, str]):
        time = str(user_feedback['time'])
        date = str(user_feedback['date'])
        user_email = str(user_feedback['user_email'], )
        user_input = user_feedback['user_input']
        response_received = user_feedback['response_received']
        feedback = user_feedback['feedback']

        conn = sqlite3.connect('hrb_user_feedback.db')
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
