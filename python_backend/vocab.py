# import ShellScriptExecuter
from Google_Sheet_API import GoogleSheetConnect

from pprint import pprint
import random
import re


class Node:
    def __init__(self, prev=None):
        self.prev = prev
        self.next = None

    def getNext(self):
        return self.next

    def getPrev(self):
        return self.prev

    def setNext(self, next):
        self.next = next

    def setPrev(self, prev):
        self.prev = prev

    def __str__(self):
        return "a Node"


class UnitNode(Node):
    def __init__(self, unitNum):
        self.unitNum = unitNum

    def getUnitNum(self):
        return self.unitNum

    def __str__(self):
        return "Unit_" + str(self.unitNum)

    def getType(self):
        return "unit"

    def __eq__(self, other):
        if (other):
            if(other.getType() == "unit"):
                return self.unitNum == other.getUnitNum()
            else:
                return False
        else:
            return False

    def to_dictionary(self):
        unit_dic = {}
        unit_dic.setdefault("unitNum", self.unitNum)
        unit_dic.setdefault("unitName", "unit_"+str(self.unitNum))
        return unit_dic


class Vocab(Node):
    def __init__(self, text, definition, vocabRoot, errorCount, importancy):
        super().__init__()
        self.text = text.rstrip()
        self.definition = definition
        self.vocabRoot = vocabRoot
        self.errorCount = errorCount
        self.importancy = importancy
        self.synonym = []

        # ID is for better use
        self.id = None

    def addErrorCount(self):
        self.errorCount += 1

    def getErrorCount(self):
        return self.errorCount

    def __equal__(self, text):
        return self.text == text

    def setId(self, id):
        self.id = id

    def getId(self):
        return self.id

    def getDef(self):
        return self.definition

    def getText(self):
        return self.text

    def testFormat(self):
        str = " ' " + self.text + " ' : "
        return str

    def __str__(self):
        str = self.text + " : " + self.definition + \
            " [ " + self.vocabRoot + " ]   Wrong : " + \
            self.errorCount + " Importantcy : " + self.importancy
        return str

    def getType(self):
        return "vocab"

    def to_dictionary(self):
        vocab_dic = {}
        vocab_dic.setdefault("text", self.text)
        vocab_dic.setdefault("definition", self.definition)
        vocab_dic.setdefault("vocabRoot", self.vocabRoot)
        vocab_dic.setdefault("errorCount", self.errorCount)
        vocab_dic.setdefault("importancy", self.importancy)
        return vocab_dic


class VocabControler:
    # firstVocab : root of the vocab Linked List
    def __init__(self):
        self.firstVocab = None

    def setFirstVocab(self, firstVocab):
        self.firstVocab = firstVocab

    def getFirstVocab(self):
        return self.firstVocab

    def getVocabById(self, id):
        curNode = self.firstVocab
        while(curNode):
            if(curNode.getType() != "vocab"):
                curNode = curNode.getNext()
            elif(curNode.getId() == id):
                return curNode
            else:
                curNode = curNode.getNext()
        return None

    def getVocabByText(self, text):
        curNode = self.firstVocab
        while(curNode):
            if (curNode.getType() == "vocab"):
                if (curNode.getText() == text):
                    return curNode
            curNode = curNode.getNext()

        return None

    def getVocabListLength(self, vocabOnly=False):
        curNode = self.firstVocab
        length = 0
        while(curNode):
            if (curNode.getType() == "vocab"):
                length += 1

            elif (not vocabOnly):
                length += 1
            curNode = curNode.getNext()
        return length

    def getUnitNode(self, unitNum):
        curNode = self.firstVocab
        while(curNode):
            if(curNode.getType() == "unit"):
                if(curNode.getUnitNum() == unitNum):
                    return curNode
            curNode = curNode.getNext()

        return None

    # get all the vocabs in the unit
    # returns a list of vocab

    def getVocabListInUnit(self, unitNum):
        curNode = self.getUnitNode(unitNum)
        stopNode = self.getUnitNode(unitNum+1)
        vocabList = []
        if curNode:
            while(curNode):
                if(curNode.getType() == "unit"):
                    if(curNode == stopNode):
                        break
                elif(curNode.getType() == "vocab"):
                    vocabList.append(curNode)
                curNode = curNode.getNext()
            return vocabList
        else:
            return None

    # return a list of all unit nodes
    def getAllUnits(self):
        curNode = self.firstVocab
        allUnits = []
        while(curNode):
            if(curNode.getType() == "unit"):
                allUnits.append(curNode.to_dictionary())
            curNode = curNode.getNext()

        return allUnits

    def getAllVocabText(self):
        curNode = self.firstVocab
        allVocab = []
        while(curNode):
            if(curNode.getType() == "vocab"):
                allVocab.append(curNode.getText())
            curNode = curNode.getNext()
        return allVocab
    # text: the target vocab

    # def printVocabError(self, text):
    #     curNode = self.firstVocab
    #     while(curNode.getNext() != None):
    #         if(curNode.__equal__(text)):
    #             print(curNode.getErrorCount())
    #             break
    #         curNode = curNode.getNext()
    #     print("No such vocab")

    def printAllVocab(self):
        curNode = self.firstVocab
        while(curNode):
            print(curNode)
            curNode = curNode.getNext()

    def printAllVocabDict(self):
        curNode = self.firstVocab
        while(curNode):
            if (curNode.getType() != "unit"):
                print(curNode.to_dictionary())
            curNode = curNode.getNext()


class TestQuestion:
    # vocab : the vocab that is going to be tested, options : array with 3 definition
    def __init__(self, vocab, options):
        self.vocab = vocab
        self.options = options
        self.ans = ""

    def getOptions(self):
        return self.options

    def getOptionsTestFormat(self):
        # copy the option list because (shuffledOption = self.option is passByReference)
        shuffledOption = self.options.copy()
        ansDef = self.vocab.getDef()
        shuffledOption.append(ansDef)
        random.shuffle(shuffledOption)
        testFormat = ""
        for i in range(len(shuffledOption)):
            # set the ans attribute
            if shuffledOption[i] == ansDef:
                self.setAns(i)

            testFormat += "\t" + str(i) + ". " + shuffledOption[i] + "\n"

        return testFormat.rstrip()

    def getVocabTestFormat(self):
        return self.vocab.testFormat()

    def getVocabStr(self):
        return self.vocab.__str__()

    def setAns(self, ans):
        self.ans = ans

    def getAns(self):
        return self.ans

    def to_dictionary(self):
        tq_dict = {}
        tq_dict.setdefault("vocab", self.vocab.to_dictionary())
        tq_dict.setdefault("options", self.options)
        return tq_dict


class TestQuestionCreator():
    def __init__(self, vocabControler, defPool):
        self.vocabControler = vocabControler
        self.defPool = defPool

    def create(self, vocab):
        options = self.__createOptions(vocab.getId())
        test_q = TestQuestion(vocab, options)
        return test_q

    # def createById(self, id):
    #     options = self.__createOptions(id)
    #     test_q = TestQuestion(self.vocabControler.getVocabById(id), options)
    #     return test_q

    def __createOptions(self, id_excluded):
        length = self.vocabControler.getVocabListLength(vocabOnly=True)
        options = []
        while (len(options) < 3):
            index = random.randint(0, length-1)
            if index == id_excluded or (index in options):
                continue
            else:
                options.append(index)
        for i in range(len(options)):
            index_def = self.defPool.get(options[i])
            assert (index_def != None), "Test_Question options contains None type"
            options[i] = index_def

        return options


class Test:

    # testQueue : a queue of TestQuestion object
    def __init__(self):
        self.testQueue = []
        self.wrongList = []
        self.testLength = 0

    def test(self):
        # shuffle testQueue
        # random.shuffle(self.testQueue)
        # calculate how many questions user have answered
        userAnsCount = 0
        try:
            userInput = ""
            while(userInput.upper() != 'Q'):
                curTQ = self.testQueue.pop(0)
                print("-----------------------------------")
                print(userAnsCount+1, "/", self.testLength)
                print(curTQ.getVocabTestFormat())
                input("see options")
                print(curTQ.getOptionsTestFormat())
                userInput = input("Please enter your answer: ").upper()
                # wrong ans
                if(userInput == "Q"):
                    break
                elif(userInput != str(curTQ.getAns())):
                    print("Wrong" + "\u2717")
                    self.wrongList.append(curTQ)
                    self.seeQuestionAns(curTQ)
                else:
                    print("Correct" + "	\u2713")
                userAnsCount += 1
            self.__printTestResult(userAnsCount)
            self.resetTest()
        except IndexError:
            print("Finish Test")
            self.__printTestResult(userAnsCount)
            self.resetTest()

    def seeQuestionAns(self, testQuestion):
        print(testQuestion.getVocabStr())

    def clearTestQueue(self):
        self.testQueue.clear()
        self.testLength = 0

    def appendToTestQueue(self, testQuestion):
        self.testQueue.append(testQuestion)
        self.testLength += 1

    def clearWrong(self):
        self.wrongList.clear()

    def __printTestResult(self, ansCount):
        print("-----------------------------------")
        self.__printTestStats(ansCount)
        self.__printWrongList()

    def __printWrongList(self):
        print("Wrong List -------------")
        for i in self.wrongList:
            print(i.getVocabStr())

    def __printTestStats(self, ansCount):
        wrongNum = len(self.wrongList)
        correctNum = ansCount - wrongNum
        print(str(correctNum) + "/" + str(ansCount) +
              "--------------- Total:" + str(self.testLength))

    def resetTest(self):
        self.clearWrong()
        self.clearTestQueue()
        self.testLength = 0

    def getTestQueue(self):
        return self.testQueue

    def to_dictionary(self):
        app_dic = {}
        test_queue_dic = []
        print(len(self.testQueue))
        for i in range(len(self.testQueue)):
            test_queue_dic.append(self.testQueue[i].to_dictionary())
        app_dic.setdefault("testQueue", test_queue_dic)
        return app_dic


class FileParser:
    def __init__(self):
        self.defPool = {}

    # legacy Code Parse from local
    def parseFromLocal(self, file):
        f = open(file, "r")
        vocabId = 0
        prevNode = None
        firstNode = None
        for i in f:
            line = i.split(",")
            regexCheck = re.search(
                "(Text)|(Unit_\d)|(^\s*$)", line[0])

            curNode = None

            if(regexCheck):
                unitCheck = re.search("Unit_\d", line[0])
                if (unitCheck):
                    unitNum = unitCheck.string[5:]
                    curNode = UnitNode(int(unitNum))

            elif (not regexCheck):
                curNode = Vocab(line[0], line[1], line[2],
                                line[3], line[4].rstrip())
                # give vocab an ID
                curNode.setId(vocabId)
                self.defPool.setdefault(vocabId, line[1])
                vocabId += 1
            if(curNode):
                if(not prevNode):
                    firstNode = curNode
                else:
                    curNode.setPrev(prevNode)
                    prevNode.setNext(curNode)
                prevNode = curNode

        return firstNode

    def parseFromCloud(self):
        fetchedData = GoogleSheetConnect.fetchEverySheetData()
        vocabId = 0
        prevNode = None
        firstNode = None
        for i in fetchedData[1:]:
            curNode = None
            if(len(i) != 0):
                unitCheck = re.search("Unit_\d", i[0])
                if(unitCheck):
                    unitNum = unitCheck.string[5:]
                    curNode = UnitNode(int(unitNum))
                else:
                    while(len(i) < 5):
                        i.append("")
                    curNode = Vocab(i[0], i[1], i[2],
                                    i[3], i[4])
                    # give vocab an ID
                    curNode.setId(vocabId)
                    self.defPool.setdefault(vocabId, i[1])
                    vocabId += 1
                if(curNode):
                    if(not prevNode):
                        firstNode = curNode
                    else:
                        curNode.setPrev(prevNode)
                        prevNode.setNext(curNode)
                    prevNode = curNode
        return firstNode

    def getDefPool(self):
        return self.defPool


def App(vocabControler, defPool, test):
    print("Welcome to GRE_Vocab_Tester.")
    while(True):
        # display menu
        print("Please select a mode\n\t(T) Testing Mode\n\t(D) Dictionary Mode\n\t(Q) Quit")
        menuInput = input()

        if(menuInput.upper() == "Q"):
            break
        elif (menuInput.upper() == "T"):
            # Display Test Menu
            testMode(vocabControler, defPool, test)

        elif (menuInput.upper() == "D"):
            # Display Dictionary Menu
            dictionaryMode(vocabControler)
        else:
            continue


def testMode(vocabControler, defPool, test):
    print("Test Mode ")
    unitInput = input(
        "Please Select a unit (input 'all' to test every unit): ")
    if(unitInput != 'all'):
        startUnitNode = vocabControler.getUnitNode(int(unitInput))
        endUnitNode = vocabControler.getUnitNode(int(unitInput) + 1)
        if(startUnitNode):
            TQ_Creater = TestQuestionCreator(vocabControler, defPool)
            curNode = startUnitNode
            while(not(curNode == endUnitNode)):
                if(curNode.getType() == "vocab"):
                    tq = TQ_Creater.create(curNode)
                    test.appendToTestQueue(tq)
                curNode = curNode.getNext()
            test.test()
        else:
            print("None")
    else:
        TQ_Creater = TestQuestionCreator(vocabControler, defPool)
        curNode = vocabControler.getFirstVocab()
        while(curNode):
            if(curNode.getType() == "vocab"):
                tq = TQ_Creater.create(curNode)
                test.appendToTestQueue(tq)
            curNode = curNode.getNext()
        test.test()


def dictionaryMode(vocabControler):
    print("Dictionary Mode")
    # map for cache
    searchedVocab = {}
    while (True):
        print("Type in the vocabulary to look up it's definition. Type in Q to quit Dictionary Mode")
        userInput = input()
        if(userInput.upper() == "Q"):
            break
        else:
            result = vocabControler.getVocabByText(userInput)
            print()
            if(result):
                searchedVocab.setdefault(userInput, result)
                print(result)
            else:
                print("This word don't exist in the dictionary\n")


def main():
    # Update csv file by ShellScriptExecuter
    # ShellScriptExecuter.executeScript()

    # Initiate FileParser
    FP = FileParser()
    # Initiate VocabControler
    VC = VocabControler()

    vocabHead = FP.parseFromCloud()

    VC.setFirstVocab(vocabHead)

    defPool = FP.getDefPool()

    Test = Test()

    App(VC, defPool, Test)


# def server_get_all_question(vocabControler, defPool, test):
#     TQ_Creater = TestQuestionCreator(vocabControler, defPool)
#     curNode = vocabControler.getFirstVocab()
#     while(curNode):
#         if(curNode.getType() == "vocab"):
#             tq = TQ_Creater.create(curNode)
#             test.appendToTestQueue(tq)
#         curNode = curNode.getNext()
#     pprint(test.to_dictionary())
#     return test.to_dictionary()


# def serverStart():
#     FP = FileParser()
#     # Initiate VocabControler
#     VC = VocabControler()

#     vocabHead = FP.parseFromCloud()

#     VC.setFirstVocab(vocabHead)

#     defPool = FP.getDefPool()

#     Test = Test()

#     all_testQ = server_get_all_question(VC, defPool, Test)

#     return all_testQ


# TODO: testing for making this file a class and created in Web_Server.py
# fileParser,
class Server():
    def __init__(self, fileParser, vocabControler, defPool, test):
        self.fileParser = fileParser
        self.vocabControler = vocabControler
        self.defPool = defPool
        self.test = test

        # initialize TestQuestionCreator object
        self.TQ_Creator = TestQuestionCreator(
            self.vocabControler, self.defPool)

        # store the parsed item that might need to be used later
        self.all_test_json = None

        # parse all vocab from cloud
        vocabHead = self.fileParser.parseFromCloud()
        # assign head of the linked list
        self.vocabControler.setFirstVocab(vocabHead)

    def getAllUnits(self):
        allUnit = self.vocabControler.getAllUnits()
        for i in allUnit:
            pprint(i)
        return allUnit

    def getAllTestQuestion(self):
        if self.all_test_json == None:
            curNode = self.vocabControler.getFirstVocab()
            while(curNode):
                if(curNode.getType() == "vocab"):
                    tq = self.TQ_Creator.create(curNode)
                    self.test.appendToTestQueue(tq)
                curNode = curNode.getNext()
            testDictionary = self.test.to_dictionary()
            self.all_test_json = testDictionary
            return self.all_test_json
        else:
            return self.all_test_json

    def getTestQuestionByUnit(self, unitNum):
        vocabInUnit = self.vocabControler.getVocabListInUnit(unitNum)
        # clear the testQueue in test
        self.test.clearTestQueue()
        for i in vocabInUnit:
            tq = self.TQ_Creator.create(i)
            self.test.appendToTestQueue(tq)
        test_json = self.test.to_dictionary()
        return test_json

    def getVocabText(self):
        allVocabText = self.vocabControler.getAllVocabText()
        return allVocabText

    def getVocabByText(self, text):
        return self.vocabControler.getVocabByText(text)

    def getFileParser(self):
        return self.fileParser

    def getVocabControler(self):
        return self.vocabControler

    def getDefPool(self):
        return self.defPool

    def getTest(self):
        return this.getTest


if __name__ == '__main__':
    main()
