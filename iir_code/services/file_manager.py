import pickle

from bs4 import BeautifulSoup
from iir_code.inverted_index import InvertedIndex


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
    _saved_index_path = "../"
    _current_xml_file_index = 0
    _xml_files_count = 1

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

    def get_text_from_doc_id(self, doc_id: int, filename: str) -> str:
        """
        Returns the text associated with an article id (doc_id).
        :param doc_id: The document id to find the corresponding text of
        :param filename: The filename of the file where the article is stored
        :return: The contents of the <bdy> tag
        """
        with open(self._article_file_path + str(filename), 'r') as f:
            data_stream = f.read()

        data = BeautifulSoup(data_stream, 'lxml')
        article_tag = data.find('id', text=doc_id)
        text = article_tag.parent.parent.find('bdy').text
        return text
