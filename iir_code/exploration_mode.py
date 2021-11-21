"""
This file contains your code for the interactive exploration mode where a string can be input by a user and a ranked list of documents is returned.
Make sure that the user can switch between TF-IDF and BM25 scoring functions.
"""


def main():
    function_type = input('Choose your preferred scoring function (Enter TF-IDF or BM25):')
    if function_type == "TF-IDF":
        tf_idf()
    elif function_type == "BM25":
       bm25()
    else:
        print("No valid scoring function is selected")

def tf_idf():

def bm25():


main()
