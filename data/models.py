from dataclasses import dataclass
from enum import Enum


@dataclass
class DBItem(object):
    def __init__(self): pass
    id: int


@dataclass
class User(DBItem):
    username : str
    email: str
    edu_level: str
    sessions: list
    flashcards: list


class QuestionType(Enum):
    MULTIPLE_CHOICE = 'multiple choice'
    MULTIPLE_SELECT = 'multiple select'
    FILL_IN_THE_BLANK = 'fill in the blank'
    TRUE_OR_FALSE = 'true or false'

    @staticmethod
    def getTypes():
        return (QuestionType.MULTIPLE_SELECT.value, QuestionType.MULTIPLE_CHOICE.value,
                QuestionType.FILL_IN_THE_BLANK.value, QuestionType.TRUE_OR_FALSE.value)

@dataclass
class Question(DBItem):
    question_type: object
    question: str
    answer: object
    options: list

@dataclass
class Flashcard(DBItem):
    subject: str
    question: object
    hint: str
    correct: bool

@dataclass
class Session(DBItem):
    user : object
    start_time: str
    end_time: str
    wrong_answered: int
    right_answered: int
    results : object

@dataclass
class SessionResults(DBItem):
    session_id: int
    flashcards: dict


class ResponseModel(dict):
    def __init__(self, error=False, messages=[], code=200, data={}):
        super().__init__(error=error, messages=messages, code=code, data=data)
