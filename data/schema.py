import sqlite3
from data import models


class Schema(object):
    def __init__(self, connection):
        self._connection = connection
        self.__call__()


    def __initUsersTbl(self):
        cursor = self._connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY NOT NULL,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL, 
            password TEXT NOT NULL,
            education_level TEXT);
        ''')
        cursor.close()


    def __initEducationLevelsTbl(self):
        values = ['less than high school', 'high school diploma or GED', 'some college, no degree',
                  'postsecondary certificate', 'associate\'s', 'bachelor\'s', 'master\'s', 'PhD']
        cursor = self._connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS education_levels(
            id INTEGER PRIMARY KEY NOT NULL,
            name TEXT UNIQUE NOT NULL);
        ''')
        try:
            eduVals = [(v,) for v in values]
            cursor.executemany('''INSERT INTO education_levels VALUES(NULL, ?)''', eduVals)
        except sqlite3.IntegrityError:
            pass
        cursor.close()


    def __initQuestionTypesTbl(self):
        cursor = self._connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS question_types(
            id INTEGER PRIMARY KEY  NOT NULL,
            name TEXT UNIQUE NOT NULL);
        ''')
        try:
            qTypes = [(t,) for t in models.QuestionType.getTypes()]
            cursor.executemany('''INSERT INTO question_types VALUES(NULL, ?);''', qTypes)
        except sqlite3.IntegrityError:
            pass
        cursor.close()


    def __initQuestionsTbl(self):
        cursor = self._connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS questions(
            id INTEGER PRIMARY KEY  NOT NULL,
            type TEXT NOT NULL REFERENCES question_types(name), 
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            options TEXT);
        ''')
        cursor.close()


    def __initSubjectsTbl(self):
        cursor = self._connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS subjects(
            id INTEGER PRIMARY KEY NOT NULL,
            user_id INTEGER REFERENCES users(id),
            name TEXT NOT NULL,
            UNIQUE (user_id, name));
        ''')
        cursor.close()


    def __initFlashcardsTbl(self):
        cursor = self._connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS flashcards(
            subject TEXT REFERENCES subjects(name),
            user_id INTEGER NOT NULL,
            question_id INTEGER NOT NULL,
            question TEXT REFERENCES questions(question),
            hint TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (question_id) REFERENCES questions(id),
            PRIMARY KEY (user_id, question_id));''')
        cursor.close()


    def __initCardGroupTbl(self):
        cursor = self._connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS card_groups(
            id INTEGER PRIMARY KEY  NOT NULL,
            subject TEXT NOT NULL,
            user INTEGER NOT NULL REFERENCES users(id),
            question INTEGER NOT NULL,
            FOREIGN KEY(user, question) REFERENCES flashcards(user_id, question_id));
        ''')
        cursor.close()


    def __initSessionsTbl(self):
        cursor = self._connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS sessions(
            id INTEGER PRIMARY KEY  NOT NULL,
            user_id INTEGER NOT NULL REFERENCES users(id),
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            num_cards INTEGER NOT NULL);
        ''')
        cursor.close()


    def __initSessionResultsTbl(self):
        cursor = self._connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS result_keys(
            id INTEGER PRIMARY KEY,
            result TEXT UNIQUE NOT NULL);
        ''')
        try:
            cursor.execute('''INSERT INTO result_keys VALUES(NULL, 'correct');''')
            cursor.execute('''INSERT INTO result_keys VALUES(NULL, 'incorrect');''')
        except sqlite3.IntegrityError:
            pass
        cursor.execute('''CREATE TABLE IF NOT EXISTS session_results(
            id INTEGER PRIMARY KEY ,
            session_id INTEGER NOT NULL,
            flashcard_id INTEGER NOT NULL,
            user INTEGER NOT NULL,
            answered_wrong INTEGER,
            answered_right INTEGER,
            FOREIGN KEY(session_id) REFERENCES sessions(id),
            FOREIGN KEY(user, flashcard_id) REFERENCES flashcards(user_id, question_id));
        ''')
        cursor.close()


    def __call__(self):
        self.__initEducationLevelsTbl()
        self.__initUsersTbl()
        self.__initQuestionTypesTbl()
        self.__initQuestionsTbl()
        self.__initSubjectsTbl()
        self.__initFlashcardsTbl()
        self.__initCardGroupTbl()
        self.__initSessionsTbl()
        self.__initSessionResultsTbl()
        self._connection.commit()
        self._connection.close()
        print('Schema created ')

