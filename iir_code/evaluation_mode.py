"""
This file contains your code to generate the evaluation files that are input to the trec_eval algorithm.
"""
import subprocess

from iir_code.exploration_mode import read_index_from_file, tf_idf, bm25
from iir_code.services.file_manager import FileManager

file_manager = FileManager()


def main_evaluation():
    print("Read topic file")
    topics = file_manager.read_topics_file()
    
    # Read the index
    print("Read index file")
    index = read_index_from_file()

    # TF-IDF Exploration
    process_topics_query(topics, "TF-IDF", index)

    # BM25 Exploration
    process_topics_query(topics, "BM25", index)


def perform_search(input_str: str, function_type: str, index):
    """
    Performs the search in the exploration file
    :param input_str: The search string with the title and the description of the topic
    :param function_type: The function type, could be BM25 or TF-IDF
    :param index: the inverted index
    :return: A dictionary of the result {doc_id:score} for each doc_id and for input_string
    """
    dictionary = {}
    
    if function_type == "TF-IDF":
        dictionary = tf_idf(input_str, index)
    
    elif function_type == "BM25":
        dictionary = bm25(input_str, index)

    return dictionary


def save_qrel_file(qrel_lines, function_type: str):
    """
    Performs the save of qrel files
    :return:
    """
    print("Writing qrel file for " + function_type)
    file_manager.save_qrels_file(qrel_lines, function_type)

    process_trec_eval(function_type)


def process_trec_eval(function_type: str):
    """
    Peforms
    Install trec_eval first: https://github.com/usnistgov/trec_eval or brew install trec_eval
    Ideal result should around 0.17 for TF-IDF and 0.23 for BMF
    """
    print("Trec eval for " + function_type)
    rel_info_file = "../dataset/eval.qrels"  # + function_type
    results_file = "../dataset/qrels/"+function_type+".qrels"
    subprocess.run(["trec_eval", "-m", "map", "-m", "ndcg_cut.10", "-m", "P.10", "-m", "recall.10", rel_info_file, results_file])


def process_topics_query(topics: dict, function_type: str, index):
    """
    # TODO: Check trec eval implementation
    :param function_type: The function type, could be BM25 or TF-IDF
    :param topics: The topics from the xml file
    """
    print("Starting " + function_type)
    qrels_lines = []
    for topic, sub_dictionary in topics.items():
        results = perform_search(sub_dictionary["title"] + " " + sub_dictionary["description"], function_type, index)
        # sort index by score values
        results = dict(sorted(results.items(), key=lambda item: item[1], reverse=True))
        for result_key, result_value in list(results.items())[:100]:
            rank = list(results.keys()).index(result_key) # get rank as index
            line = topic + " Q0 " + str(result_key) + " " + str(rank) + " " + str(result_value) + " " + function_type
            # print(line)
            qrels_lines.append(line)

    save_qrel_file(qrels_lines, function_type)


# main_evaluation()
process_trec_eval("BM25")
process_trec_eval("TF-IDF")