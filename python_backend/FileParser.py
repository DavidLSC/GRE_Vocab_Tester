from Google_Sheet_API import GoogleSheetConnect

import vocab

from pprint import pprint
import random
import re


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
                curNode = vocab.Vocab(line[0], line[1], line[2],
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
                    curNode = vocab.UnitNode(int(unitNum))
                else:
                    while(len(i) < 5):
                        i.append("")
                    curNode = vocab.Vocab(i[0], i[1], i[2],
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
