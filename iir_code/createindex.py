"""
This file contains your iir_code to create the inverted index. Besides implementing and using the predefined tokenization function (text2tokens), there are no restrictions in how you organize this file.
"""
from iir_code.inverted_index import InvertedIndex
from iir_code.services.file_manager import FileManager
import re

fileManager = FileManager("../dataset/wikipedia articles/")
invertedIndex = InvertedIndex()


# cachedFiles: {int: [str]} = {}
def main():
    readAllFiles()


def readAllFiles():
    for docID in range(fileManager.getXmlFilesCount()):
        print("Read file: " + str(docID) + ".xml")
        content = fileManager.readNextXmlFile()
        processFile(content, docID)


def processFile(content: [str], docID: int):
    for text in content:
        token = text2tokens(text) # TODO: Is it one string or a array of strings?
        invertedIndex.append(token, docID)


def text2tokens(text: str):
    text = text.lower()
    splitedText = re.split(" |\n", text)
    print(splitedText)

    """
    :param text: a text string
    :return: a tokenized string with preprocessing (e.g. stemming, stopword removal, ...) applied
    """
    return ""


main()
