import os
import pickle

from bs4 import BeautifulSoup
from iir_code.data.inverted_index import InvertedIndex


def id_has_parent_header_and_associated_body(tag):
    """
    Finds all article ids which have a corresponding bdy.
    :param tag: A tag as found by beautifulsoup's find_all() method
    :return: True if the tag satisfies the requirements, False otherwise
    """
    if tag.name == 'id' and tag.parent.name == 'header' and tag.parent.find_next_sibling('bdy') is not None:
        return True
    return False


class FileManager:
    _article_file_path = "../dataset/wikipedia articles/"
    _topics_file_path = "../dataset/topics.xml"
    _saved_index_path = "../dataset/index.pickle"
    _saved_qrels_files_path = "../dataset/qrels/"
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

        article_ids = data.find_all(id_has_parent_header_and_associated_body)
        body_tags = data.find_all("bdy")

        # Remove the <bdy></bdy> and <id></id> tags from the elements
        article_ids = [tag.text for tag in article_ids]
        body_tags = [tag.text for tag in body_tags]

        # Construct a list of tuples [(id, body)] with each article id and corresponding body
        id_body_list = tuple(zip(article_ids, body_tags))

        return id_body_list

    def read_topics_file(self):
        with open(self._topics_file_path, 'r') as f:
            data_stream = f.read()

        data = BeautifulSoup(data_stream, 'lxml')
        topic_elements = data.findAll("topic")

        topics = {}

        for topic in topic_elements:
            id = topic.get('id')
            title = topic.select('title')[0].contents[0]
            description = topic.select('description')[0].contents[0]
            topics.update({id: {'title': title, 'description': description}})

        return topics

    def save_index_to_pickle(self, inverted_index: InvertedIndex):
        """
        Store an index as a pickle file in inverted_index.pickle.
        :param inverted_index: The inverted index to save to disk
        """
        with open(self._saved_index_path + 'inverted_index.pickle', 'wb') as handle:
            pickle.dump([inverted_index.dictionary, inverted_index.ranking_dict], handle,
                        protocol=pickle.HIGHEST_PROTOCOL)

    def load_index_from_pickle(self) -> InvertedIndex:
        """
        Load an index from a pickle file.
        return: The index loaded from disk
        """
        with open(self._saved_index_path + 'inverted_index.pickle', 'rb') as handle:
            index = pickle.load(handle)
            inverted_index = InvertedIndex()
            inverted_index.dictionary = index[0]
            inverted_index.ranking_dict = index[1]

            return inverted_index

    def get_text_from_doc_id(self, doc_id: int, file_number: int) -> str:
        """
        Returns the text associated with an article id (doc_id).
        :param doc_id: The document id to find the corresponding text of
        :param file_number: The number of the file where the article is stored
        :return: The contents of the <bdy> tag
        """
        with open(self._article_file_path + str(file_number) + '.xml', 'r') as f:
            data_stream = f.read()

        data = BeautifulSoup(data_stream, 'lxml')
        article_tag = data.find('id', text=doc_id)
        text = article_tag.parent.parent.find('bdy').text
        return text

    def save_qrels_file(self, qrels_lines, function_type):
        print('Save result as qrels file')
        base_path = self._saved_qrels_files_path + function_type
        with open(base_path + ".qrels", 'wb') as handle:
            handle.write('\n'.join(qrels_lines).encode('utf-8'))

        # os.rename(base_path + ".txt", base_path + ".qrels")  # Can take some seconds until file is available
