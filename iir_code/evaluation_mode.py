"""
This file contains your code to generate the evaluation files that are input to the trec_eval algorithm.
"""
from iir_code.services.file_manager import FileManager

run_name = "007"
file_manager = FileManager()


def main_exploration():
    topics = file_manager.read_topics_file()
    process_topics_query(topics)


def print_query_result(topic_id, document_id, rank, score):
    print(topic_id + " Q0 " + document_id + " " + rank + " " + score + " " + run_name)


def process_topics_query(topics: dict):
    """
    # TODO: Get the top 100 ranked and scored results from tf_idf or bm25 / wait till this part is implemented
    # TODO: Adjust to the corresponding result parameters
    :param topics:
    """
    for topic, sub_dictionary in topics.items():
        print(sub_dictionary["title"] + " " + sub_dictionary["description"])
        # results = tf_idf(sub_dictionary["title"] + " " + sub_dictionary["description"], 100)
        # for result in results:
        #    print_query_result(topic, result["document_id"], result["rank"], result["score"])


main_exploration()
