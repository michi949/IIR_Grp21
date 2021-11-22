import pickle

from bs4 import BeautifulSoup
from iir_code.data.inverted_index import InvertedIndex
from iir_code.data.topic import Topic


class FileManager:
    _article_file_path = "../dataset/wikipedia articles/"
    _topics_file_path = "../dataset/topics.xml"
    _saved_index_path = "index.pickle"
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

        return id_body_list

    def read_topics_file(self):
        with open(self._topics_file_path, 'r') as f:
            data_stream = f.read()

        data = BeautifulSoup(data_stream, 'lxml')
        topic_elements = data.findAll("topic")

        topics = []

        for topic in topic_elements:
            id = topic.get('id')
            title = topic.select('title')[0].contents[0]
            description = topic.select('description')[0].contents[0]
            topics.append(Topic(id, title, description))

        return topics

    def save_index_as_pickle(self, inverted_index: InvertedIndex):
        print('Dumping index to disk...')
        with open(self._saved_index_path, 'wb') as handle:
            pickle.dump(inverted_index.dictionary, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def load_index_from_pickle(self):
        print('Loading index from disk')

        with open(self._saved_index_path, 'rb') as handle:
            return pickle.load(handle)
