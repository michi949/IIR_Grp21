import gensim
from sklearn.metrics.pairwise import cosine_similarity

def get_model(path):
    return gensim.models.KeyedVectors.load_word2vec_format(path, binary=False, encoding='utf8')

def warmup(model):
    """Get most similar words."""
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

