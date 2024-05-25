import sqlite3
from typing import *
import hashlib


class AuthUser:
    def hash_password(self, password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def check_user(self, email: Any, password: Any):
        conn = sqlite3.connect('hrbuddy_users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        if user:
            hashed_input_password = self.hash_password(password)
            if hashed_input_password == user[2]:
                return True
        else:
            print("User Does Not Exist")
            return False

    def create_user(self, email, password):
        conn = sqlite3.connect('hrbuddy_users.db')
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')

        hashed_password = self.hash_password(password)

        cursor.execute(
            'INSERT INTO users (email, password) VALUES (?, ?)', (email, hashed_password))

        conn.commit()
        conn.close()


# if __name__ == '__main__':
#     auth = AuthUser()
#     auth.create_user('hr_user1@jio.com', '05022024')
