import numpy as np


class InvertedIndex(object):
    dictionary = {}

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

    def append_list(self, tokens: [str], doc_id: int):
        """
        Append each token in tokens to the index and set the doc_id.
        :param tokens: The list of tokens to add
        :param doc_id: The document id
        """
        for token in tokens:
            self.append(token, doc_id)

    def sort_index(self):
        """Sort the index by tokens in-place."""
        sorted_dictionary = {}
        for i in sorted(self.dictionary):
            sorted_dictionary[i] = self.dictionary[i]
        self.dictionary = sorted_dictionary
