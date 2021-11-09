class DictionaryEntry:
    _token: str
    _posting: [int] = []


class InvertedIndex:
    _dictionary: [DictionaryEntry] = []

    def append(self):
        pass

    def sortIndex(self):
        pass

    def checkDoubleToken(self, token: str):
        pass
