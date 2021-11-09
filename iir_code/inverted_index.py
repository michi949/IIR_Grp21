import json


class DictionaryEntry(object):
    token: str
    posting: [int]

    def __init__(self, token: str, dicID: int):
        self.token = token
        self.posting = []
        self.posting.append(dicID)

    def findDocIdInPostings(self, docID):
        for i in self.posting:
            if i == docID:
                return i
        return -1

    def sortDocIDs(self):
        self.posting.sort()


class InvertedIndex(object):
    dictionary: [DictionaryEntry] = []

    def append(self, token: str, docID: int):
        index = self.findIndexOfEntry(token)

        if index == -1:
            entry = DictionaryEntry(token, docID)
            self.dictionary.append(entry)
            self.sortIndex()
        elif 0 <= index < len(self.dictionary):
            if self.dictionary[index].findDocIdInPostings(docID) == -1:
                self.dictionary[index].posting.append(docID)
                self.dictionary[index].sortDocIDs()

    def sortIndex(self):
        self.dictionary = sorted(self.dictionary, key=lambda x: x.token)

    def checkDoubleToken(self, token: str):
        pass

    def findIndexOfEntry(self, token: str):
        for i, entry in enumerate(self.dictionary):
            if entry.token == token:
                return i
        return -1
