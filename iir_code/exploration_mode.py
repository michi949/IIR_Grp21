"""
This file contains your code for the interactive exploration mode where a string can be input by a user and a ranked list of documents is returned.
Make sure that the user can switch between TF-IDF and BM25 scoring functions.
"""
from iir_code.services.file_manager import FileManager

file_manager = FileManager()

def main():
    input_str = input('Pleas enter your search input string:')
    function_type = input('Choose your preferred scoring function (Enter TF-IDF or BM25):')

    if function_type == "TF-IDF":
        tf_idf(input_str)
    elif function_type == "BM25":
        bm25(input_str)
    else:
        print("No valid scoring function is selected")


def read_index_from_file():
    """
    Read the data from file to perform the exploration
    :return: Returns the index from file
    """
    return file_manager.load_index_from_pickle()

def read_topic_file():
    return file_manager.read_topics_file()


def tf_idf(input_str: str):
    """
    Performs the TF-IDF exploration mode
    :param input_str: The search input string
    """
    index = read_index_from_file()



def bm25(input_str: str):
    """
    Performs the BM25 exploration mode
    :param input_str: The search input string
    """
    index = read_index_from_file()



# main()
read_topic_file()
