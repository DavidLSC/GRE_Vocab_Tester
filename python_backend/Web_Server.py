from flask import Flask, request, jsonify
from flask_cors import CORS
# import json
import vocab
import VocabControler
import FileParser
from User import UserControler

app = Flask(__name__)

# allow cross origin
CORS(app)

# initialize FileParser
fileParser = FileParser.FileParser()
vocabControler = VocabControler.VocabControler()
defPool = fileParser.getDefPool()
test = vocab.Test()

# TODO: still testing usercontroler function
userControler = UserControler.UserController()

# initialize server object
Server = vocab.Server(fileParser, vocabControler, defPool, test, userControler)

# TODO: make a standard return json Object
# {
# status: ok/error
# message:
# }


@app.route('/', methods=['GET'])
def welcome():
    return "<h1>/testAll to get all test questions<h1>"


@app.route('/getAllUnits', methods=['GET'])
def get_all_units():
    allUnit = Server.getAllUnits()
    return jsonify(allUnit)


@app.route('/getAllTest', methods=['GET'])
def get_all_test():
    allTest = Server.getAllTestQuestion()
    return jsonify(allTest.get("testQueue"))


@app.route('/getTestByUnit/<int:unit_num>', methods=['GET'])
def get_test_by_unit(unit_num):
    testByUnit = Server.getTestQuestionByUnit(unit_num)
    return jsonify(testByUnit.get("testQueue"))


@app.route('/getAllVocabText', methods=['GET'])
def get_all_vocab_text_only():
    allVocabText = Server.getVocabText()
    return jsonify(allVocabText)


@app.route('/getVocabByText/<string:vocab_text>', methods=['GET'])
def get_vocab_by_text(vocab_text):
    targetVocab = Server.getVocabByText(vocab_text)
    if(targetVocab == None):
        errorMessage = {"status": "error", "message": "no such vocab"}
        return errorMessage
    else:
        data = targetVocab.to_dictionary()
        data["status"] = "ok"
        return jsonify(data)


# addErrorCount request data
# {
#     "text": vocab_text,
#     "errorCount" : error_number_needed_to_be_added
# }
@app.route('/addErrorCount', methods=['POST'])
def addErrorCount():
    jsonData = request.get_json(force=True)
    targetVocab = Server.getVocabByText(jsonData["text"])
    if(targetVocab):
        targetVocab.addErrorCount(int(jsonData["errorCount"]))
        print(targetVocab, jsonData)
        json = {
            "status": "ok",
            "message": targetVocab.getText() + "'s error number is" + str(targetVocab.getErrorCount())
        }
        return jsonify(json)
    else:
        return jsonify({
            "status": "error",
            "message": "can't find vocab " + jsonData["text"]
        })

# addSampleSentence request data
# {
#     "text": vocab_text,
#     "sentence" : sample_sentence
# }


@app.route("/addSampleSentence", methods=["POST"])
def addSampleSentence():
    jsonData = request.get_json(force=True)
    targetVocab = Server.getVocabByText(jsonData["text"])
    if(targetVocab):
        # TODO: sample sentence
        print(jsonData["sentence"])
        return jsonify({
            "status": "ok",
            "message": targetVocab.getText() + " add new sample sentence"
        })
    else:
        return jsonify({
            "status": "error",
            "message": "can't find vocab " + jsonData["text"]
        })


# ModifyPersonalList request data
# {
#     "text": vocab_text,
#     "username" : username,
#     "userId" : userId
# }
@app.route("/ModifyPersonalList", methods=["POST"])
def ModifyPersonalList():
    jsonData = request.get_json(force=True)
    # TODO: create userFile.py and add the vocabID to the list
    print(jsonData["text"], jsonData["userId"],
          jsonData["username"], jsonData["add"])
    userControler = Server.getUserControler()
    auth = userControler.authenticate(
        id=jsonData["userId"], name=jsonData["username"])
    if(auth):
        if(jsonData["add"]):
            return jsonify({
                "status": "ok",
                "message": jsonData["text"] + " has been added to your list"
            })
        else:
            return jsonify({
                "status": "ok",
                "message": jsonData["text"] + " has been removed from your list"
            })
    else:
        return jsonify({
            "status": "error",
            "message": "authentication error"
        })

# USER ACCOUNT ENDPOINT

# login request data
# {
#       "userName": username
#       "password": password
# }


@app.route("/login", methods=["POST"])
def login():
    jsonData = request.get_json(force=True)
    userName = jsonData["username"]
    password = jsonData["password"]
    userControler = Server.getUserControler()
    targetUser = userControler.getUserByName(userName)
    if(targetUser):
        if(targetUser.checkPassword(password)):
            return jsonify({
                "status": "ok",
                "message": "Welcome " + userName,
                "userData": targetUser.getData(),
                "userId": targetUser.getId()
            })
        else:
            return jsonify({
                "status": "error",
                "message": "Username or Password is in correct, please check if you type in the correct value"
            })
    else:
        return jsonify({
            "status": "error",
            "message": "Username or Password is in correct, please check if you type in the correct value"
        })


@app.route("/createAccount", methods=["POST"])
def createAccount():
    jsonData = request.get_json(force=True)
    # {
    #   username : String,
    #   password: String,
    #   email: String
    # }
    userControler = Server.getUserControler()
    if not userControler.getUserByName(jsonData["username"]):
        createdUserData = userControler.createUser(userName=jsonData["username"],
                                                   password=jsonData["password"], email=jsonData["email"])
        print(createdUserData)
        return jsonify({
            "status": "ok",
            "message": "Account user " + jsonData["username"] + " has been created."
        })
    else:
        return jsonify({
            "status": "error",
            "message": "user " + jsonData["username"] + " already exist"
        })


@app.route("/getUserInfo", methods=["POST"])
def getUserInfo():
    #{username: String}
    jsonData = request.get_json(force=True)
    userControler = Server.getUserControler()
    target = userControler.getUserByName(jsonData["username"])
    if target:
        data = target.to_dictionary()
        return jsonify({
            "status": "ok",
            "data": data,
            "message": "user " + jsonData["username"] + ' exist'
        })
    else:
        return jsonify({
            "status": "error",
            "message": "user don't exist"
        })


@app.route("/test")
def test():
    testVal = [{'vocab': {'text': 'fathom', 'definition': '??????', 'vocabRoot': '',
                          'errorCount': '0', 'importancy': '5'}, 'options': ['????????????????????????????????????', '??????', '?????????']}]
    return jsonify(testVal)


if __name__ == '__main__':
    app.run()
