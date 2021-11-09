from bs4 import BeautifulSoup
from iir_code.inverted_index import InvertedIndex, DictionaryEntry
import json

class FileManager:
    _articleFilePath = "../dataset/wikipedia articles/"
    _savedIndexPath = "../"
    _currentXmlFileIndex = 0
    _xmFilesCount = 553

    def __init__(self):
        self._currentXmlFileIndex = 0

    def getXmlFilesCount(self):
        return self._xmFilesCount

    def readNextXmlFile(self):
        self._currentXmlFileIndex += 1
        return self.readXmlFile(self._currentXmlFileIndex)

    def readXmlFile(self, index: int):
        contentArray: [str] = []

        with open(self._articleFilePath + str(index) + ".xml", 'r') as f:
            dataStream = f.read()

        data = BeautifulSoup(dataStream, 'lxml')
        bodyElements = data.findAll("bdy")

        # TODO [MiRe] Add description headers
        for ele in bodyElements:
            for content in ele.contents:
                contentArray.append(content)

        return contentArray

    def saveInvertedIndexToJson(self, invertedIndex: InvertedIndex):
        jsonDic: {str: [int]} = {}

        for entry in invertedIndex.dictionary:
            jsonDic[entry.token] = entry.posting

        with open(self._savedIndexPath + "invertedIndex.json", "w") as outfile:
            json.dump(jsonDic, outfile)

    # TODO: Check why sometime value dupplicated in array
    def loadInvertedIndexFromJson(self):
        with open(self._savedIndexPath + "invertedIndex.json", "r") as f:
            data = json.load(f)

            invertedIndex = InvertedIndex()
            for key in data:
                print(key)
                print(data[key])
                invertedIndex.dictionary.append(DictionaryEntry(key, data[key]))

            return invertedIndex