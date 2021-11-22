"""
This file contains your code to generate the evaluation files that are input to the trec_eval algorithm.
"""
from iir_code.exploration_mode import tf_idf, bm25
from iir_code.services.file_manager import FileManager

file_manager = FileManager()


def main_exploration():
    topics = file_manager.read_topics_file()

    # TF-IDF Exploration
    process_topics_query(topics, "TF-IDF")

    # BM25 Exploration
    process_topics_query(topics, "BM25")


def perform_search(input_str: str, function_type: str):
    """
    Performs the search in the exploration file
    :param input_str: The search string with the title and the description of the topic
    :param function_type: The function type, could be BM25 or TF-IDF
    :return: A dictionary of the result
    """
    if function_type == "TF-IDF":
        return tf_idf(input_str)
    elif function_type == "BM25":
        return bm25(input_str)
    else:
        return {}


def process_trec_eval(qrel_lines, function_type: str):
    """
    Performs the trec evaluation
    Ideal result should around 0.17 for TF-IDF and 0.23 for BMF
    :return:
    """
    file_manager.save_qrels_file(qrel_lines, function_type)


def process_topics_query(topics: dict, function_type: str):
    """
    # TODO: Get the top 100 ranked and scored results from tf_idf or bm25 / wait till this part is implemented
    # TODO: Adjust to the corresponding result parameters
    :param function_type: The function type, could be BM25 or TF-IDF
    :param topics: The topics from the xml file
    """
    qrels_lines = []
    for topic, sub_dictionary in topics.items():
        results = perform_search(sub_dictionary["title"] + " " + sub_dictionary["description"], function_type)
        for result_key, result_value in results.items():
            line = topic + " Q0 " + result_key["document_id"] + " " + result_value["rank"] + " " + result_value[
                "score"] + " " + function_type

            print(line)
            qrels_lines.append(line)

    process_trec_eval(qrels_lines, function_type)


# main_exploration()
process_trec_eval(["2010003 Q0 19243417 1",
                   "2010003 Q0 3256433 1",
                   "2010003 Q0 275014 1",
                   "2010003 Q0 298021 0"], "TD-IFD")
