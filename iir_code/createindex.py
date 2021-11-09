"""
This file contains your iir_code to create the inverted index. Besides implementing and using the predefined tokenization function (text2tokens), there are no restrictions in how you organize this file.
"""
from iir_code.inverted_index import InvertedIndex
from iir_code.services.file_manager import FileManager

fileManager = FileManager("../dataset/wikipedia articles/")
invertedIndex = InvertedIndex()


# cachedFiles: {int: [str]} = {}


def readAllFiles():
    for count in range(fileManager.getFilesCount()):
        print("Read file: " + str(count) + ".xml")
        content = fileManager.readNextFile()
        processFile(content)


def processFile(content: [str]):
    for text in content:
        token = text2tokens(text)
        invertedIndex.append(token)


def text2tokens(text):
    """
    :param text: a text string
    :return: a tokenized string with preprocessing (e.g. stemming, stopword removal, ...) applied
    """
    return ""


readAllFiles()
