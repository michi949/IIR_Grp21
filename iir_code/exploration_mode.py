"""
This file contains your code for the interactive exploration mode where a string can be input by a user and a ranked list of documents is returned.
Make sure that the user can switch between TF-IDF and BM25 scoring functions.
"""

# IMPORTANT: change this file when the duplicates in the postings lists are fixed

from FileManager import FileManager
from createindex import text2tokens
import numpy as np


file_manager = FileManager()


def main():
    input_str = input('Please enter your search input string:')
    function_type = input('Choose your preferred scoring function (Enter TF-IDF or BM25):')
    n_docs_to_return = input('Choose the number of most relevant documents you wish to be returned:')
    
    index = read_index_from_file()
    
    if function_type == "TF-IDF":
        dict_scores = tf_idf(input_str, index)
    elif function_type == "BM25":
        dict_scores = bm25(input_str, index)
    else:
        print("No valid scoring function is selected")
        print("Default Method is TF-IDF")
        dict_scores = tf_idf(input_str, index)
            
    if len(n_docs_to_return) == 0:
        print("No valid number of documents is selected")
        print("Default number is 1")
        n_docs_to_return = '1'
    
    # sort dictionary by values (scores)
    sorted_score_dict = dict(sorted(dict_scores.items(), key=lambda item: item[1], reverse=True))
    
    for i in range(int(n_docs_to_return)):
        doc_id = list(sorted_score_dict.keys())[i]
        print("Document ranked in position: ", i+1)
        print("Score value: %f" % (dict_scores[doc_id],))
        print(file_manager.get_text_from_doc_id(doc_id, index.ranking_dict[doc_id][1]))
    

def read_index_from_file():
    """
    Read the data from file to perform the exploration
    :return: Returns the index from file
    """
    return file_manager.load_index_from_pickle()


def tf_idf(input_str: str, index):
    """
    Performs the TF-IDF exploration mode
    :param input_str: The search input string
    :param doc_id: a document ID 
    :param index: the index returned from file
    """ 
    query_processed = text2tokens(input_str)
    N = len(index.ranking_dict)
    tfidf_dict = {}
    for doc_id in index.ranking_dict.keys():
        score_tfidf = 0
        for token in query_processed:
            if token in index.dictionary.keys() and doc_id in index.dictionary[token][::2]:
                df_t = len(index.dictionary[token]) / 2
                tf_td = index.dictionary[token][np.where(index.dictionary[token] == doc_id)[0][0] + 1]
                tfidf = np.log(1+tf_td)*np.log(N/df_t)
                score_tfidf += tfidf
        tfidf_dict[doc_id] = score_tfidf
    return tfidf_dict


def bm25(input_str: str, index, k1=1.2, b=0.75):
    """
    Performs the BM25 exploration mode
    :param input_str: The search input string
    :param doc_id: a document ID 
    :param index: the index returned from file
    :param k1: k1 parameter for bm25
    :param b: b parameter for bm25
    """
    query_processed = text2tokens(input_str)
    N = len(index.ranking_dict)
    bm25_dict = {}
    L_ave = np.array([int(index.ranking_dict[doc_id][0]) for doc_id in index.ranking_dict]).mean()
    for doc_id in index.ranking_dict.keys():
        score_bm25 = 0
        for token in query_processed:
            if token in index.dictionary.keys() and doc_id in index.dictionary[token][::2]:
                df_t = len(index.dictionary[token]) / 2
                L_d = int(index.ranking_dict[doc_id][0])
                tf_td = index.dictionary[token][np.where(index.dictionary[token] == doc_id)[0][0] + 1]
                score_bm25 += np.log(N/df_t)*(((k1+1)*tf_td)/(k1*((1-b)+b*(L_d/L_ave))+tf_td))
        bm25_dict[doc_id] = score_bm25
    return bm25_dict

#main()

