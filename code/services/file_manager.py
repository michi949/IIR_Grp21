from bs4 import BeautifulSoup

class FileManager:
    _filePath = "../../dataset/wikipedia articles/"
    _currentFileIndex = 0

    def __init__(self):
        self._currentFileIndex = 0

    def readNextFile(self):
        self._currentFileIndex += 1
        return self.readFile(self._currentFileIndex)

    def readFile(self, index: int):
        contentArray: [str] = []

        with open(self._filePath + str(index) + ".xml", 'r') as f:
            dataStream = f.read()

        data = BeautifulSoup(dataStream, 'lxml')
        bodyElements = data.findAll("bdy")

        # TODO [MiRe] Improve Code
        for ele in bodyElements:
            for content in ele.contents:
                contentArray.append(content)

        return contentArray
