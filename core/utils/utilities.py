import json
import jwt
import re
import requests
import bcrypt
import functools
from icecream import ic
from data import ResponseModel
from flask import jsonify, request


class AuthUtil(object):
    ''' This class is responsible for most authentication functionality. '''
    @staticmethod
    def getHash(password, salt=bcrypt.gensalt()):
        return bcrypt.hashpw(password.encode(), salt)


    @staticmethod
    def validateSignInPassword(dao, email, passwd):
        storedPass = dao.queryUserPass(email.lower())
        match = AuthUtil.getHash(passwd, salt=storedPass) == storedPass
        return (True, 'Incorrect password provided.') if not match else (False, None)


    @staticmethod
    def validateSignInEmail(dao, email):
        found = dao.queryUserEmail(email) == email.lower()
        return (True, 'Couldn\'t find a user with this email.') if not found else (False, None)


    @staticmethod
    def isStrongPass(password):
        # a strong password is at least 7 to 20 characters of at least a single capital letter, symbol and digit.
        pattern = re.compile('^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[^a-zA-Z0-9])(?!.*\s).{7,20}$')
        ic(pattern)
        if pattern.match(password) is None:
            return False
        else:
            return True


    @staticmethod
    def authRequired(app):
        '''Magic. Do not touch! Provides protection for routes requiring user authorization.'''
        def authDecorator(f):
            @functools.wraps(f)
            def wrapped(*args, **kwargs):
                token = request.headers['Authorization']
                if not token:
                    return jsonify(ResponseModel(error=True, messages=['No token provided']))
                try:
                    jwt.decode(token, app.secret_key, algorithms=['HS256'])
                except jwt.InvalidTokenError:
                    return jsonify(ResponseModel(error=True, messages=['Invalid token provided!']))
                return f(*args, **kwargs)
            return wrapped
        return authDecorator


    @staticmethod
    def generateToken(email, appDAO, appContext):
        return jwt.encode(
            AuthUtil.getPayload(email, appDAO), appContext.secret_key, algorithm='HS256').decode('utf-8')


    @staticmethod
    def decodeToken(token, app):
        if token:
            try:
                data = jwt.decode(token, app.secret_key)
                return ResponseModel(error=False, messages=['jwt decode success'], code=200, data=data)
            except jwt.InvalidTokenError:
                return ResponseModel(error=True, messages=['Invalid token provided'], code=404)


    @staticmethod
    def getPayload(email, dao):
        payload = { 'user': dao.retrieveUser(email.lower()).__dict__ }
        print(f'payload: {payload}')
        return payload


    @staticmethod
    def validateSignupEmail(dao, email):
        ''' :param   dao: object used for accessing the database.
            :param email: user's email used for registration.
            :returns: authorization status as a tuple of the error's state: True or False, and message
        '''
        pattern = re.compile('^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))'
                             '([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$')
        if pattern.match(email) is None:
            return True, 'Email address format invalid.'
        if dao.queryUserEmail(email) is not None:
            return True, 'Email address already exists.'
        else:
            return False, None


    @staticmethod
    def validateSignupPassword(passwd, rePasswd):
        ''':param    passwd: the raw user password input
           :param    rePasswd: the re-entry confirmation of user password input.
           :returns  tuple: (False, None) or (True, 'Error message').
        '''
        if passwd != rePasswd:
            return True, 'Passwords do not match.'
        else:
            if not AuthUtil.isStrongPass(passwd):
                return True, 'Password must contain 7 to 20 characters of at least\na single capital letter, symbol and digit.'
        return False, None


    @staticmethod
    def getSignInResponse(dao, email, password):
        emailStatus = AuthUtil.validateSignInEmail(dao, email)
        if emailStatus[0] is True:  # if a user's email isn't found
            response = ResponseModel(error=True, messages=[emailStatus[1], None], code=404)
        else:  # if a user's email is found, but password is incorrect
            passwdStatus = AuthUtil.validateSignInPassword(dao, email, password)
            if passwdStatus[0] is True:
                response = ResponseModel(error=True, messages=[None, passwdStatus[1]], code=404)
            else:
                response = ResponseModel(error=False, messages=[None, None], code=200)
        return response


    @staticmethod
    def getUserSignUpResponse(dao, **kwargs):
        ''':param    dao: object used for database access.
           :param kwargs: user filled parameters from registration form.
           :returns: Dict - Error indicator and status message of user submitted registration info.
        '''
        data = {
            'user': kwargs.get('username'), 'email': kwargs.get('email'),
            'passwd': kwargs.get('passwd'), 'rePasswd': kwargs.get('rePasswd')
        }
        emailStatus = AuthUtil.validateSignupEmail(dao, data['email'])
        passwdStatus = AuthUtil.validateSignupPassword(data['passwd'], data['rePasswd'])
        return ResponseModel(
            error=emailStatus[0] or passwdStatus[0], messages=[emailStatus[1], passwdStatus[1]]
        )


    @staticmethod
    def getAppKey(filePath):
        with open(filePath, 'r') as txtFile:
            return json.loads(txtFile.read())['secret_key']



class WordUtil(object):
    ''' interfaces with an API for generating results for filler content such as
        dummy answers for questions, similar words, autogenerated and supplemental text.
        Also for verifying correct text punctuation grammar, and spelling.
    '''
    def __init__(self):
        self._datamuseURL = 'https://api.datamuse.com'
        self._perfectTenseURL = 'https://api.perfecttense.com'
        self._credentials = self.__initCredentials('../project_mindbeam/data/credentials/creds.json')
        self._fillerQueryRef = {
            'similar_meaning': '/words?ml=',
            'similar_sounding': '/words?sl=',
            'similar_spelling': '/words?sp=',
            'descriptive_adjective': '/words?rel_jjb=',
            'often_described_by': '/words?rel_jja=',
            'often_followed_by': '/words?lc='
        }
        self._correctionApiHeaders = {
            'Authorization': self._credentials['apikey'],
            'AppAuthorization': self._credentials['appkey'],
            'Content-Type': 'application/json'
        }


    def __initCredentials(self, filepath):
        with open(filepath, 'r') as textfile:
             return json.loads(textfile.read())


    def getSimilarMeaning(self, word):
        url = self._buildFillerQuery(word, self._fillerQueryRef['similar_meaning'])
        return requests.get(url).json()


    def getSimilarSounding(self, word):
        url = self._buildFillerQuery(word, self._fillerQueryRef['similar_sounding'])
        return requests.get(url).json()


    def getSimilarSpelling(self, word):
        url = self._buildFillerQuery(word, self._fillerQueryRef['similar_spelling'])
        return requests.get(url).json()


    def getDescriptiveAdjs(self, word):
        url = self._buildFillerQuery(word, self._fillerQueryRef['descriptive_adjective'])
        return requests.get(url).json()


    def getOftenDescribedBy(self, word):
        url = self._buildFillerQuery(word, self._fillerQueryRef['often_described_by'])
        return requests.get(url).json()


    def getOftenFollowedBy(self, word):
        url = self._buildFillerQuery(word, self._fillerQueryRef['often_followed_by'])
        return requests.get(url).json()


    def getCorrectedText(self, text):
        data = {
            'text': text, 'responseType': ['corrected', 'grammarScore', 'rulesApplied', 'offset', 'summary']
        }
        response = requests.post(
            f'{self._perfectTenseURL}/correct', headers=self._correctionApiHeaders, data=json.dumps(data)
        )
        dictRep = json.loads(response.text)
        return dictRep['corrected']


    def _buildFillerQuery(self, word, queryRef):
        return self._datamuseURL + queryRef + word

def printRequestInfo(req):
    print(f"Request:\n{req}\n")
    print(f"headers:\n{req.headers}\n")
    print(f"auth:\n{req.authorization}\n")
    print(f"mimetype:\n{req.mimetype}\n")
    print(f"form:\n{req.form}\n")
    print(f"data:\n{req.data}\n")
    print(f"files:\n{req.files}\n")

