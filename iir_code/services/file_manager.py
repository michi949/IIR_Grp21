import json
from bs4 import BeautifulSoup
from iir_code.inverted_index import InvertedIndex


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

    def read_xml_file(self, index: int) -> [(str, str)]:
        with open(self._article_file_path + str(index) + ".xml", 'r') as f:
            data_stream = f.read()

        data = BeautifulSoup(data_stream, 'lxml')
        body_elements = data.findAll("bdy")
        article_id_elements = data.select('header > id')

        # Remove the <bdy></bdy> and <id></id> tags from the elements
        bodies_cleaned = [tag.contents[0] for tag in body_elements]
        ids_cleaned = [tag.contents[0] for tag in article_id_elements]

        # Construct a list of tuples [(id, body)] with each article id and corresponding body
        id_body_list = tuple(zip(ids_cleaned, bodies_cleaned))

        # TODO [MiRe] Add description headers

        return id_body_list

    def save_index_to_json(self, inverted_index: InvertedIndex):
        """
        Store an index as a json file.
        :param inverted_index: The index to be saved
        """
        """
        json_dic: {str: [int]} = {}

        for token in inverted_index.dictionary.keys():
            json_dic[token] = inverted_index.dictionary.get(token).tolist()

        """
        with open(self._saved_index_path + "inverted_index.json", "w") as outfile:
            json.dump(inverted_index.dictionary, outfile)

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
                inverted_index.append(key, data[key])

            return inverted_index
