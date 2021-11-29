import numpy as np


class InvertedIndex(object):
    dictionary = {}
    ranking_dict = {}

    def append(self, token: str, doc_id: int):
        """
        Append a document id to a token's postings list.
        :param token: The token to be added
        :param doc_id: The document id
        """
        current_postingslist = self.dictionary.get(token)
        if current_postingslist is None:
            self.dictionary.update({token: np.array([doc_id], dtype=np.int16)})
        else:
            self.dictionary.update({token: np.append(current_postingslist, doc_id)})

    def append_dict(self, tokens: dict, doc_id: int, length: int, filename: str):
        """
        Set the frequency of a token occurring in a specific article (document) and
        record the length and filename of the article.
        :param tokens: Dictionary with all tokens and their frequency in the article with doc_id
        :param doc_id: ID of the article
        :param length: Length of the article in words/terms
        :param filename: Filename of the file in which the article is stored
        """
        for token in tokens:
            if token in self.dictionary:
                # Set the frequency of token occurring in article with doc_id
                self.dictionary[token][doc_id] = tokens[token]
            else:
                self.dictionary[token] = {doc_id: 1}
        self.ranking_dict[doc_id] = np.array([length, filename])

    def sort_index(self):
        """Sort the index by tokens in-place."""
        sorted_dictionary = {}
        for i in sorted(self.dictionary):
            sorted_dictionary[i] = self.dictionary[i]
        self.dictionary = sorted_dictionary
