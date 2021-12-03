"""
This file contains your code to generate the evaluation files that are input to the trec_eval algorithm.
"""
import subprocess

from exploration_new import tf_idf, bm25, read_index_from_file
from FileManager import FileManager

file_manager = FileManager()


def main_exploration():
    topics = file_manager.read_topics_file()
    
    # Read the index
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


def process_trec_eval(qrel_lines, function_type: str):
    """
    Performs the trec evaluation
    Install trec_eval first: https://github.com/usnistgov/trec_eval or brew install trec_eval
    Ideal result should around 0.17 for TF-IDF and 0.23 for BMF
    :return:
    """
    file_manager.save_qrels_file(qrel_lines, function_type)

    base_path = "../dataset/eval.qrels"  # + function_type
    goal_path = "../retrieval_results/" + function_type.lower() + "_title_description.txt"
    subprocess.run(["trec_eval", "-m", "map", "-m", "ndcg_cut.10", "-m", "P.10", "-m", "recall.10", base_path, goal_path])


def process_topics_query(topics: dict, function_type: str, index):
    """
    # TODO: Check trec eval implementation
    :param function_type: The function type, could be BM25 or TF-IDF
    :param topics: The topics from the xml file
    """
    qrels_lines = []
    for topic, sub_dictionary in topics.items():
        results = perform_search(sub_dictionary["title"] + " " + sub_dictionary["description"], function_type, index)
        # sort index by score values
        results = dict(sorted(results.items(), key=lambda item: item[1], reverse=True))
        for result_key, result_value in list(results.items())[:100]:
            rank = list(results.keys()).index(result_key) # get rank as index
            line = topic + " Q0 " + str(result_key )+ " " + str(rank) + " " + str(result_value) + " " + function_type
            # print(line)
            qrels_lines.append(line)

    process_trec_eval(qrels_lines, function_type)


main_exploration()
process_trec_eval(["2010003 Q0 19243417 1",
                   "2010003 Q0 3256433 1",
                   "2010003 Q0 275014 1",
                   "2010003 Q0 298021 0"], "TD-IFD")

