from pprint import pprint
import random
import re


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
