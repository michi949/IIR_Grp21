from bs4 import BeautifulSoup
from iir_code.inverted_index import InvertedIndex
from types import SimpleNamespace
import json

class FileManager:
    _articleFilePath = "../../dataset/wikipedia articles/"
    _savedIndexPath = "../"
    _currentXmlFileIndex = 0
    _xmFilesCount = 553

    def __int__(self):
        self._currentXmlFileIndex = 0

    def __init__(self, articleFilePath: str):
        self._currentXmlFileIndex = 0
        self._articleFilePath = articleFilePath

    def getXmlFilesCount(self):
        return self._xmFilesCount

    def readNextXmlFile(self):
        self._currentFileIndex += 1
        return self.readXmlFile(self._currentXmlFileIndex)

    def readXmlFile(self, index: int):
        contentArray: [str] = []

        with open(self._filePath + str(index) + ".xml", 'r') as f:
            dataStream = f.read()

        data = BeautifulSoup(dataStream, 'lxml')
        bodyElements = data.findAll("bdy")

        # TODO [MiRe] Add description headers
        for ele in bodyElements:
            for content in ele.contents:
                contentArray.append(content)

        return contentArray

    # TODO: Fix that stuff
    def saveInvertedIndexToJson(self, invertedIndex: InvertedIndex):
        with open(self._savedIndexPath + "invertedIndex.json", "w") as outfile:
            json.dump(invertedIndex, outfile)


    def loadInvertedIndexFromJson(self):
        with open(self._savedIndexPath + "invertedIndex.json", "r") as f:
            x = json.loads(f, object_hook=lambda d: SimpleNamespace(**d))
            print(x)
