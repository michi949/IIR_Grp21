"""
This file contains your code to generate the evaluation files that are input to the trec_eval algorithm.
"""
from iir_code.services.file_manager import FileManager

file_manager = FileManager()


def main():
    topics = file_manager.read_topics_file()
    print(topics)


main()
