import gensim
import os
from sklearn.metrics.pairwise import cosine_similarity

# wiki-news-300d-1M-subword.vec unzipped locally
model_file = os.path.join('..', 'dataset', 'wiki-news-300d-1M-subword.vec')
model = gensim.models.KeyedVectors.load_word2vec_format(model_file, binary=False, encoding='utf8')

# Define pairs of words and compute cosine similarity
pairs=[["cat","dog"], ["cat","Vienna"], ["Vienna","Austria"],
       ["Austria","dog"]]

for pair in pairs:
  first = model[pair[0]]
  second = model[pair[1]]
  cossim = cosine_similarity([first], [second])[0]
  print(pair, cossim)
  
# Find top 3 most similar words
print("Top 3 Vienna: ", model.most_similar("Vienna", topn=3))
print("Top 3 Austria: ", model.most_similar("Austria", topn=3))
print("Top 3 cat: ", model.most_similar("cat", topn=3))
