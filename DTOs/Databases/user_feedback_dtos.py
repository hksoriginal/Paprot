from dataclasses import dataclass


@dataclass
class UserFeedbackDTO:
    time: str
    date: str
    user_email: str
    user_input: str
    response_received: str
    time_taken: str
    feedback: str
