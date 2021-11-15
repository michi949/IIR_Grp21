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

file_manager = FileManager()
inverted_index = InvertedIndex()

# stop words set
sw_set = set(stopwords.words('english'))
sw_set.update({''})  # add as stop words to remove empty strings

# punctuation
regular_punct = string.punctuation
extra_punct = [',', '.', '"', ':', ')', '(', '!', '?', '|', ';', "'", '$', '&',
               '/', '[', ']', '>', '%', '=', '#', '*', '+', '\\', '•', '~', '@', '£',
               '·', '_', '—', '{', '}', '©', '^', '®', '`', '<', '→', '°', '€', '™', '›',
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
    read_all_files()


def read_all_files():
    """Read all XML files stored in the '../dataset/wikipedia articles' directory."""
    for doc_id in range(file_manager.get_xml_files_count()):
        print("Read file: " + str(doc_id) + ".xml")
        content = file_manager.read_next_xml_file()
        process_file(content, doc_id)


def process_file(content: [str], doc_id: int):
    """
    Reads in content, converts it to tokens and writes them to the index.
    :param content: The contents of the <bdy> tag from the XML file
    :param doc_id: The id of the XML file
    """
    for text in content:
        token = text2tokens(text)
        inverted_index.append_list(token, doc_id)
        

def remove_accents(text):
    """
    Substitutes accents with non-accents letters in text.
    : param text: The text to be analized
    """
    text = re.sub(u"[àáâãäå]", 'a', text)
    text = re.sub(u"[èéêë]", 'e', text)
    text = re.sub(u"[ìíîï]", 'i', text)
    text = re.sub(u"[òóôõö]", 'o', text)
    text = re.sub(u"[ùúûü]", 'u', text)
    text = re.sub(u"[ýÿ]", 'y', text)
    text = re.sub(u"[ß]", 'ss', text)
    text = re.sub(u"[ñ]", 'n', text)  
    return text 


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
    
    # remove accents
    text = remove_accents(text)

    # remove all \xa chars
    text = unicodedata.normalize("NFKD", text)

    # handle multi-blanks
    text = re.sub(' +', ' ', text)

    # remove punctuation
    text = text.translate(str.maketrans('', '', punctuation))

    # tokenization
    splitted_text = re.split(" |\n", text)

    # stemming 
    PS = PorterStemmer()
    splitted_text = [PS.stem(token) for token in splitted_text]

    # stop words removal
    splitted_text = [token for token in splitted_text if token not in sw_set]

    return splitted_text


main()
