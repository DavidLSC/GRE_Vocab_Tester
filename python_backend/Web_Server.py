from flask import Flask, request, jsonify
from flask_cors import CORS
# import json
import vocab
import VocabControler
import FileParser

app = Flask(__name__)

# allow cross origin
CORS(app)

# initialize FileParser
fileParser = FileParser.FileParser()
vocabControler = VocabControler.VocabControler()
defPool = fileParser.getDefPool()
test = vocab.Test()

# initialize server object
Server = vocab.Server(fileParser, vocabControler, defPool, test)


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


@app.route("/test")
def test():
    testVal = [{'vocab': {'text': 'fathom', 'definition': '理解', 'vocabRoot': '',
                          'errorCount': '0', 'importancy': '5'}, 'options': ['危險的、背叛的、不可靠的', '揭露', '貧乏的']}]
    return jsonify(testVal)


if __name__ == '__main__':
    app.run()
