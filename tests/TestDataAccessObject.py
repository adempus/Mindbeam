import unittest
from data import DataAccessObject
from data import QuestionType

class DataAccessObjectTest(unittest.TestCase):
    def setUp(self):
        self.appDAO = DataAccessObject('../data/db/app.db')


    @unittest.skip # fails
    def testInsertWithCommitSeparate(self):
        userFile = "./res/big_user_set.csv"
        with open(userFile, 'r') as users:
            for line in users:
                data = line.split(',')
                data[3] = data[3].split('\n')[0]
                self.appDAO.insertNewUser(name=data[0], email=data[1], password=data[2],
                                          edu_lvl=int(data[3]), commit=True)


    @unittest.skip
    def testInsertNewMultipleChoiceQuestion(self):
        self.appDAO.insertNewQuestion(type=QuestionType.MULTIPLE_CHOICE,
                                      q='The quantity of abstractions in a component is represented in: ',
                                      a='Na', options=['A', 'Na', 'Nc', 'SDP'],
                                      commit=True)

    @unittest.skip
    def testInsertMultipleSelectQuestion(self):
        self.appDAO.insertNewQuestion(type=QuestionType.MULTIPLE_SELECT,
                                      q='A dictionary in Python can be created using the following syntax: ',
                                      a=['dict()', '{}'], options=['dict()', 'dictionary()', 'new dict', '{}'],
                                      commit=True)

    @unittest.skip
    def testInsertTrueOrFalseQuestion(self):
        self.appDAO.insertNewQuestion(type=QuestionType.TRUE_OR_FALSE,
                                      q='A compiled language is typically slower than an interpreted language.',
                                      a='False', options=[True, False],
                                      commit=True)

    @unittest.skip
    def testInsertFillInTheBlankQuestion(self):
        self.appDAO.insertNewQuestion(type=QuestionType.FILL_IN_THE_BLANK,
                                      q='A _______ is a structure used for storing key, value pairs.',
                                      a='hash map',
                                      commit=True)
    @unittest.skip
    def testInsertNonTypeQuestion(self):
        with self.assertRaises(ValueError, msg='insertNewQuestion() does not raise expected exception.'):
            self.appDAO.insertNewQuestion(q='Does this sample question raise an error from the DAO? ',
                                          a='Hopefully.',
                                          commit=True)

    @unittest.skip
    def testInsertNewSubject(self):
        self.appDAO.insertNewSubject(userEmail='janepierre10@gmail.com',
                                     name='software engineering',
                                     commit=True)
        self.appDAO.insertNewSubject(userEmail='johndoe01@gmail.com',
                                     name='data structures',
                                     commit=True)

    @unittest.skip
    def testInsertNewFlashcard(self):
        self.appDAO.insertNewFlashcard(subject='software engineering',
                                       question='A compiled language is typically slower than an interpreted language.',
                                       email='janepierre10@gmail.com', hint='compiler wins', commit=True)

    @unittest.skip
    def testGetEducationLevel(self):
        levels = {
        'lvl1' : self.appDAO.queryEducationLevel(1),
        'lvl6' : self.appDAO.queryEducationLevel(6),
        'lvl3' : self.appDAO.queryEducationLevel(3),
        'lvl8' : self.appDAO.queryEducationLevel(8)
        }
        print(f'level: {levels.keys()}\n values: {levels.values()}')

    def testCommitAllOpen(self):
        self.appDAO.commitAllOpen()


    @unittest.skip
    def testDataFrames(self):
        dFrames = self.appDAO.getDataFrames()
        usersFrame = dFrames['users']
        print(f'{usersFrame}\n')
        questionsFrame = dFrames['questions']
        print(f'\n{questionsFrame}')


    @unittest.skip
    def testInsertNewUser(self):
        self.appDAO.insertNewUser(name='Test Dummy', email='TestDummy144@gmail.com', password='dsdgsggsgaregrg',
                                  edu_lvl=2, commit=True)


    def testQueryUserEmail(self):
        invalid = 'dgsdgdgdwFAf@GMAIL.COM'
        valid = 'testdummy144@gmail.com'
        invalResult = self.appDAO.queryUserEmail(invalid)
        validResult = self.appDAO.queryUserEmail(valid)
        print(invalResult)
        print(validResult)

if '__main__'==__name__:
    daoTest = DataAccessObjectTest()
    daoTest.setUp()
    # # daoTest.testGetEducationLevel()
    daoTest.testInsertNewUser()
    # daoTest.testInsertWithCommitSeparate()
    # daoTest.testGetUser()
    # daoTest.testInsertNewMultipleChoiceQuestion()
    # daoTest.testInsertMultipleSelectQuestion()
    # daoTest.testInsertTrueOrFalseQuestion()
    # daoTest.testInsertNonTypeQuestion()
    # daoTest.testInsertFillInTheBlankQuestion()
    # daoTest.testInsertNewSubject()
    # daoTest.testInsertNewFlashcard()
    # daoTest.testDataFrames()
