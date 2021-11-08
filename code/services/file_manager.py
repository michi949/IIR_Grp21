from bs4 import BeautifulSoup

class FileManager:
    _filePath = "../../dataset/wikipedia articles"
    _currentFileIndex = 0

    def __init__(self):
        print("FileManager is created")

    def readNextFile(self):
        self._currentFileIndex += 1
        return self.readFile(self._currentFileIndex)

    def readFile(self, index):
        return ""
