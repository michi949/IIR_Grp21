# https://github.com/t-systems-on-site-services-gmbh/german-wikipedia-text-corpus

import os
import gensim
from gensim.parsing.preprocessing import *

dataset = os.path.join('..', 'dataset', 'wiki-all-shuf.txt')
reduced_dataset = os.path.join('..', 'dataset', 'wiki-all-shuf-reduced.txt')
german_model = os.path.join('..', 'dataset', 'german.model')
chunksize = 1073741824


def read_wiki_file() -> [string]:
   """
   Read the wiki file and return an array of text blocks.
   """

   print("Read wiki file set")
   with open(reduced_dataset, "r") as f:
       data_string = f.read()
       f.close()

   return data_string.split("\n")


def reduce_wiki_file():
   """
   Reduce the 6gb wiki dataset to given chunk size.
   """
   if os.path.isfile(reduced_dataset):
       return

   with open(dataset, "rb") as f:
       chunk = f.read(chunksize)
       f.close()

   with open(reduced_dataset, "w") as w:
       w.write(chunk.decode("utf-8"))
       w.close()


def create_german_language_model(vector_size=100, window=5, min_count=1, epochs=10, workers=3):
   """
   Preprocess the text blocks and creates a german word2vec model with given settings.
   """
   FILTERS = [strip_tags, strip_punctuation, strip_multiple_whitespaces, strip_numeric, strip_short]
   texts = read_wiki_file()

   print("Preprocess dataset")
   texts_tokenized = [preprocess_string(text.lower(), FILTERS) for text in texts]

   print("Create german word2vec model")
   model = gensim.models.Word2Vec(sentences=texts_tokenized,
                                  vector_size=vector_size,
                                  window=window,
                                  min_count=min_count,
                                  epochs=epochs,
                                  workers=workers)
   model.save(german_model)


def compute_german_words():
   """
   Compute 3 German words the top-3 most similar words
   """
   model = gensim.models.Word2Vec.load(german_model)
   model_wv = model.wv

   print("Top 3 Planeten: ", model_wv.most_similar("planeten", topn=3))
   print("Top 3 Arzt: ", model_wv.most_similar("arzt", topn=3))
   print("Top 3 Winter: ", model_wv.most_similar("winter", topn=3))

