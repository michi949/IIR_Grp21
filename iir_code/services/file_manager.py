from bs4 import BeautifulSoup
from iir_code.inverted_index import InvertedIndex, DictionaryEntry
import json

class FileManager:
    _article_file_path = "../dataset/wikipedia articles/"
    _saved_index_path = "../"
    _current_xml_file_index = 0
    _xml_files_count = 553

    def __init__(self):
        self._current_xml_file_index = 0

    def get_xml_files_count(self):
        return self._xml_files_count

    def read_next_xml_file(self):
        """
        Increment the current read index and read the next file.
        :return: The contents of the next XML file
        """
        self._current_xml_file_index += 1
        return self.read_xml_file(self._current_xml_file_index)

    def read_xml_file(self, index: int):
        content_array: [str] = []

        with open(self._article_file_path + str(index) + ".xml", 'r') as f:
            data_stream = f.read()

        data = BeautifulSoup(data_stream, 'lxml')
        body_elements = data.findAll("bdy")

        # TODO [MiRe] Add description headers
        for ele in body_elements:
            for content in ele.contents:
                content_array.append(content)

        return content_array

    def save_index_to_json(self, inverted_index: InvertedIndex):
        """
        Store an index as a json file.
        :param inverted_index: The index to be saved
        """
        json_dic: {str: [int]} = {}

        for token in inverted_index.dictionary.keys():
            json_dic[token] = inverted_index.dictionary.get(token).tolist()

        with open(self._saved_index_path + "inverted_index.json", "w") as outfile:
            json.dump(json_dic, outfile)

    def load_index_from_json(self):
        """
        Load an index from a json file.
        :return: The inverted index
        """
        with open(self._saved_index_path + "inverted_index.json", "r") as f:
            data = json.load(f)

            inverted_index = InvertedIndex()
            for key in data:
                print(key)
                print(data[key])
                invertedIndex.dictionary.append(DictionaryEntry(key, data[key]))

            return inverted_index
