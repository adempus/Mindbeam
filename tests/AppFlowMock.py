import unittest
from data import *
from core import AuthUtil

class AppFlowMock(unittest.TestCase):
    def setUp(self):
        self.dao = DataAccessObject('../data/db/app.db')

    def testInitialize(self):
        print('Project Mindbeam™\n')
        option = self.testValidateRangeInput('1. Sign Up \n2. Sign In\n', 1, 2)
        if option == 1:
            self.testSignUp()
        elif option == 2:
            self.signIn()


    #TODO: continue mock application flow: https://trello.com/c/CYSaXHue/29-mock-application-flow
    def testSignUp(self):
        username = input('Enter username: ')
        email = input('Enter email: ')
        password = input('Enter Password: ')
        rePass = input('Re-enter Password: ')
        isValidPasswd = AuthUtil.validateSignInPassword(password, rePass)
        eduLvl = self.testValidateRangeInput('Enter education level: ', 1, 8)


    def signIn(self):
        pass


    def testValidateRangeInput(self, prompt, start, stop):
        option = 0
        validInput = option >= start or option <= stop
        while not validInput:
            option = input(prompt)
            if not validInput:
                print('Invalid option provided. Try again')
        return option


if __name__ == '__main__':
    print('running')
    mock = AppFlowMock()
    mock.setUp()

