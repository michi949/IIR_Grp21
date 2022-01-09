import os

from warmup import *
from short_text_similarity import *
from create_german_model import *

# wiki-news-300d-1M-subword.vec unzipped locally
model_file = os.path.join('..', 'dataset', 'wiki-news-300d-1M-subword.vec')

if __name__ == "__main__":
    model = get_model(model_file)
    warmup(model)
    short_text_similarity(model)
    reduce_wiki_file()
    create_german_language_model()
    compute_german_words()
