from .schema import Schema
from .models import QuestionType, User
from queue import Queue
import functools
import sqlite3


def singleton(cls):
    instances = dict()
    @functools.wraps(cls)
    def _singleton(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return _singleton


@singleton
class DataAccessObject(object):
    def __init__(self, dbPath):
        self.dbPath = dbPath
        self._schema = Schema(self.getConnectionCursor()[0])
        self._commitQueue = Queue()


    def insertNewUser(self, **kwargs):
        userData = {
            'name': kwargs.get('name'),
            'email': kwargs.get('email'),
            'password': kwargs.get('password')
            # 'edu_lvl': kwargs.get('edu_lvl')
        }
        if not None in userData.values():
            # userData['edu_lvl'] = self.queryEducationLevel(userData['edu_lvl'])
            con, cur = self.getConnectionCursor()
            cur.execute('''INSERT INTO users VALUES(NULL, ?, lower(?), ?, NULL);''', tuple(userData.values()))
            self.__finalize(con, cur, kwargs.get('commit'))
            name = userData['name']
            print(f'inserted new user {name} in db')


    def insertNewQuestion(self, **kwargs):
        ''' inserts a user submitted question into the database. A QuestionType enum value must be specified for type;
            q and a args. are mandatory. Options are only mandatory for Multiple Choice, and Select types.
            A list of questions may be iterated over sending each of their respective criteria passed in as kwargs
            to this method.
        '''
        questionData = {
            'type': kwargs.get('type'), 'q': kwargs.get('q'), 'a': kwargs.get('a'), 'options': kwargs.get('options')
        }
        qType = questionData['type']
        if not isinstance(qType, QuestionType):
            raise ValueError('A QuestionType enum value must be supplied for arg: \'type\'')
        else:
            con, cur = self.getConnectionCursor()
            questionData['type'] = qType.value
            if qType in [QuestionType.MULTIPLE_CHOICE, QuestionType.MULTIPLE_SELECT]:
                # stringify values to account for error prone iterable args.
                values = tuple(str(v) for v in questionData.values())
                cur.execute('''INSERT INTO questions VALUES (NULL, ?, ?, ?, ?)''', values)
            elif qType in [QuestionType.TRUE_OR_FALSE, QuestionType.FILL_IN_THE_BLANK]:
                questionData.popitem()  # omit options for defaults
                values = tuple(v for v in questionData.values())
                if qType is QuestionType.TRUE_OR_FALSE:
                    cur.execute('''INSERT INTO questions VALUES(NULL, ?, ?, ?, '[True, False]')''', values)
                else:
                    cur.execute('''INSERT INTO questions VALUES(NULL, ?, ?, ?, NULL)''', values)
            self.__finalize(con, cur, kwargs.get('commit'))


    def insertNewSubject(self, **kwargs):
        subjectData = { 'userEmail': kwargs.get('userEmail'), 'name': kwargs.get('name') }
        if not None in subjectData.values():
            con, cur = self.getConnectionCursor()
            email = subjectData.pop('userEmail')
            # print(email)
            try:
                subjectData = {**{'id': self.getIdByEmail(email)}, **subjectData}
                print(subjectData)
            except TypeError:
                raise TypeError(f'User with email: {email} does not exist')
            cur.execute('''INSERT INTO subjects VALUES(NULL, ? , ?);''',
                        tuple(v for v in subjectData.values()))
            self.__finalize(con, cur, kwargs.get('commit'))


    def insertNewFlashcard(self, **kwargs):
        '''Executed when the user chooses to create flashcards from all currently submitted questions.
           It is preferred that the question assigned to a flashcard is specified by its literal string
           value in the questions table.
         '''
        cardData = {
            'subject': kwargs.get('subject'), 'userId': None, 'questionId': None,
            'question': kwargs.get('question'), 'hint' : kwargs.get('hint'), 'email': kwargs.get('email')
        }
        if not None in [cardData['email'], cardData['question']]:
            con, cur = self.getConnectionCursor()
            cardData['userId'] = self.getIdByEmail(cardData.pop('email'))
            print(cardData['userId'])
            print(type(cardData['userId']))
            print(cardData)
            if cardData['subject'] is not None:
                cardData['subject'] = cur.execute(
                    '''SELECT name FROM subjects WHERE user_id = ? AND name = ?''',
                            (cardData['userId'], cardData['subject'])).fetchone()[0]
            cardData['questionId'] = cur.execute(
                '''SELECT id FROM questions WHERE question = ?''',
                        (cardData['question'],)).fetchone()[0]
            cur.execute(
                '''INSERT INTO flashcards VALUES(?, ?, ?, ?, ?)''', tuple(v for v in cardData.values()))
            self.__finalize(con, cur, kwargs.get('commit'))


    def getIdByEmail(self, email):
        email = email.lower()
        con, cur = self.getConnectionCursor()
        result = cur.execute('''SELECT id FROM users WHERE email = ?''', (email,)).fetchone()[0]
        self.__finalize(con, cur, close=True)
        return result


    def getEmailById(self, id):
        con, cur = self.getConnectionCursor()
        try:
            result = cur.execute('''SELECT email FROM users WHERE id = ?''', (id,)).fetchone()[0]
        except TypeError:
            return None
        self.__finalize(con, cur, close=True)
        return result


    def retrieveUser(self, email):
        con, cur = self.getConnectionCursor()
        print("entered email: "+email)
        try:
            record = cur.execute('''SELECT * FROM users WHERE email=?''', (email,)).fetchall()[0]
            self.__finalize(con, cur, close=True)
            # noinspection PyArgumentList
            foundUser = User(id=record[0], username=record[1], email=record[2], edu_level=record[4],
                             sessions=[], flashcards=[])
            return foundUser
        except Exception:
            raise ValueError('User not found. Make sure username/email and password are correct. ')


    def queryUserPass(self, email):
        if self.queryUserEmail(email):
            con, cur = self.getConnectionCursor()
            result = cur.execute('''SELECT password FROM users WHERE email = ?''', (email,)).fetchone()
            self.__finalize(con, cur, close=True)
            return None if not result else result[0]
        return None


    def queryUserEmail(self, email):
        email = email.lower()
        con, cur = self.getConnectionCursor()
        result = cur.execute('''SELECT email FROM users WHERE email=?''', (email,)).fetchone()
        self.__finalize(con, cur, close=True)
        return None if result is None else result[0]


    def queryEducationLevel(self, edu_lvl):
        con, cur = self.getConnectionCursor()
        edu_lvl = cur.execute('''SELECT name FROM education_levels WHERE id=?''', (edu_lvl, )).fetchone()[0]
        self.__finalize(con, cur, close=True)
        return edu_lvl


    def getConnectionCursor(self):
        connection = sqlite3.connect(self.dbPath)
        return connection, connection.cursor()


    def retrieveFlashcards(self, email):
        # get all flashcards with email == email.
        pass


    #TODO: https://trello.com/c/pUaJ24Uq/27-daocommitallopen
    def __finalize(self, con, cur, commit=False, close=False):
        def _close(con, cur):
            cur.close()
            con.close()
        if commit is True:
            con.commit()
            _close(con, cur)
        elif close is True:
            _close(con, cur)
        else:
            self._commitQueue.put((con, cur))


    #TODO: https://trello.com/c/pUaJ24Uq/27-daocommitallopen
    def commitAllOpen(self):
        while not self._commitQueue.empty():
            con, cur = self._commitQueue.get()
            self.__finalize(con, cur, commit=True)
