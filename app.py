from data import DataAccessObject
from core import AuthUtil, DocumentHandler, printRequestInfo
from subprocess import check_output
from flask import Flask, request, jsonify
from flask_uploads import UploadSet, configure_uploads, IMAGES
from data import ResponseModel
from datetime import datetime
from icecream import ic


ALLOWED_EXTENSIONS = {'.jpg', '.png', '.jpeg', '.pdf'}
app = Flask(__name__)
appDAO = DataAccessObject('./data/db/app.db')
app.secret_key = AuthUtil.getAppKey('./data/credentials/secretKey.json')
userUploads = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = './data/image_uploads/'
configure_uploads(app, userUploads)
authRequired = AuthUtil.authRequired
docHandler = DocumentHandler()
ic.configureOutput(includeContext=True)


@app.route('/')
def index():
    return 'Hello World!'


@app.route('/login', methods=['POST'])
def login():
    data = dict(request.get_json())
    email, passwd = data.values()
    jsonResponse = AuthUtil.getSignInResponse(appDAO, email, passwd)
    print(jsonResponse)
    if jsonResponse['error'] is False:
        payload = AuthUtil.getPayload(email, appDAO)
        jsonResponse['token'] = AuthUtil.generateToken(email, appDAO, app)
        authToken = jsonResponse['token']
        ic(f'\nuser {email} login credentials verified.\nPayload: {payload}\nAuthToken: {authToken}')
        ic(f'response: {str(jsonResponse)}\n')
        return jsonify(jsonResponse)
    else:
        print(f'\nLogin could not be verified for {email}.\n')
    return jsonify(jsonResponse)


@app.route('/register', methods=['POST'])
def register():
    data = dict(request.get_json())
    user, email, passwd, rePasswd = data.values()
    jsonResponse = AuthUtil.getUserSignUpResponse(
        appDAO, username=user, email=email, passwd=passwd, rePasswd=rePasswd
    )
    if jsonResponse['error'] is False:
        appDAO.insertNewUser(
            name=user, email=email, password=AuthUtil.getHash(passwd), commit=True
        )
        jsonResponse['messages'] = ['User registration successful!']
    ic(jsonResponse)
    return jsonify(jsonResponse)


@app.route('/authenticate', methods=['POST'])
@authRequired(app)
def authenticate():
    print(request.get_json())
    return jsonify(
        ResponseModel(error=False, messages=['User token authenticated.'], code=200)
    )


@app.route('/dashboard', methods=['POST'])
@authRequired(app)
def dashboard():
    data = dict(request.get_json()) # decode token to find the user.
    print(data)
    jwtAuth = data['jwtAuth']
    userData = AuthUtil.decodeToken(jwtAuth, app)
    print("decoded user data from jwt: "+str(userData))
    return jsonify(
        ResponseModel(error=False, messages=['Dashboard']))


@app.route('/upload', methods=['POST', 'GET'])
@authRequired(app)
def imageUpload():
    printRequestInfo(request)
    if request:
        decoded = AuthUtil.decodeToken(request.headers['Authorization'], app)
        userId = f"{decoded['data']['user']['username']}_"
        filename = userUploads.save(request.files['photo'])
        uploadPath = app.config['UPLOADED_PHOTOS_DEST']+filename
        digitizedText = docHandler.digitizeDocument(uploadPath)
        print("Digitized text: "+ digitizedText)
        return jsonify(
            ResponseModel(error=False, messages=[f"File upload: {userId+filename} successful!"],
                          data={'digitizedText': digitizedText})
        )
    return jsonify(
        ResponseModel(error=True, messages=['Image did not upload successfully']))


@app.route('/sentencize', methods=['POST'])
@authRequired(app)
def sentencizeDocument():
    reqTime = datetime.now()
    # printRequestInfo(request)
    data = dict(request.get_json())
    confirmedDoc = data.values()
    ic("confirmed document sent by user: "+str(confirmedDoc))
    if request:
        decoded = AuthUtil.decodeToken(request.headers['Authorization'], app)
        ic(f"user: {decoded['data']['user']['username']} made sentencize request @ {reqTime}")
    return jsonify(ResponseModel(error=False, messages=["sentencize request made"], data={}))


@app.route('/test', methods=['GET'])
def testRoute():
    ip = check_output(['hostname', '-I']).decode()[0:-2]
    return jsonify(
        ResponseModel(messages=[f'some jsonified test data from http://{ip}:5000/test']))


@app.route('/verify', methods=['GET'])
@authRequired(app)
def verifyJwt():
    data = request.args.get('jwt')
    print(data)
    return jsonify(
        ResponseModel(messages=[f'JWT code verified for code: {data}']))



@app.route('/fetch_test')
def fetch_test():
    return 'Any string'


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

