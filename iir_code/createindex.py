"""
This file contains your iir_code to create the inverted index. Besides implementing and using the predefined tokenization function (text2tokens), there are no restrictions in how you organize this file.
"""
from iir_code.inverted_index import InvertedIndex
from iir_code.services.file_manager import FileManager
import re
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import string
import unicodedata


fileManager = FileManager()
invertedIndex = InvertedIndex()

# stop words set
sw_set = set(stopwords.words('english'))
sw_set.update({''}) # add as stop words to remove empty strings

# punctuation
regular_punct = string.punctuation
extra_punct = [',', '.', '"', ':', ')', '(', '!', '?', '|', ';', "'", '$', '&',
    '/', '[', ']', '>', '%', '=', '#', '*', '+', '\\', '•',  '~', '@', '£',
    '·', '_', '—', '{', '}', '©', '^', '®', '`',  '<', '→', '°', '€', '™', '›',
    '♥', '←', '×', '§', '″', '′', 'Â', '█', '½', 'à', '…', '“', '★', '”',
    '–', '●', 'â', '►', '−', '¢', '²', '¬', '░', '¶', '↑', '±', '¿', '▾',
    '═', '¦', '║', '―', '¥', '▓', '—', '‹', '─', '▒', '：', '¼', '⊕', '▼',
    '▪', '†', '■', '’', '▀', '¨', '▄', '♫', '☆', 'é', '¯', '♦', '¤', '▲',
    'è', '¸', '¾', 'Ã', '⋅', '‘', '∞', '∙', '）', '↓', '、', '│', '（', '»',
    '，', '♪', '╩', '╚', '³', '・', '╦', '╣', '╔', '╗', '▬', '❤', 'ï', 'Ø',
    '¹', '≤', '‡', '√', '«', '»', '•', '´', 'º', '¾', '¡', '§', '£', '₤', 
    '€', '·']
extra_punct = "".join(extra_punct)
punctuation = regular_punct + extra_punct



# cachedFiles: {int: [str]} = {}
def main():
    readAllFiles()


def readAllFiles():
    for docID in range(fileManager.getXmlFilesCount()):
        print("Read file: " + str(docID) + ".xml")
        content = fileManager.readNextXmlFile()
        processFile(content, docID)


# TODO: Is it one string or a array of strings?
def processFile(content: [str], docID: int):
    for text in content:
        token = text2tokens(text)
        invertedIndex.append(token, docID)

# TODO: Should we remove accents (eg.: é->e)?
def text2tokens(text: str):
    """
    :param text: a text string
    :return: a tokenized string with preprocessing (e.g. stemming, stopword removal, ...) applied
    """
    
    # lowercase
    text = text.lower()
    
    # remove all http addresses and www websites
    text = re.sub("http[^\\s]+", "", text)
    text = re.sub("www[^\\s]+", "", text)
    
    # remove all \xa chars
    text = unicodedata.normalize("NFKD", text)
    
    #handle multi-blanks
    text = re.sub(' +', ' ', text)
           
    # remove punctuation
    text = text.translate(str.maketrans('', '', punctuation))
        
    # tokenization
    splitedText = re.split(" |\n", text)

    # stemming 
    PS = PorterStemmer()
    splitedText = [PS.stem(token) for token in splitedText]

    # stop words removal
    splitedText = [token for token in splitedText if token not in sw_set]

    return splitedText

main()
