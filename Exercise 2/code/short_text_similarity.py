import pandas as pd
import numpy as np
import gensim
import os
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.stats.stats import pearsonr

stop_words = set(stopwords.words('english'))
model_file = os.path.join('..', 'dataset', 'wiki-news-300d-1M-subword.vec')
model = gensim.models.KeyedVectors.load_word2vec_format(model_file, binary=False, encoding='utf8')

def preprocessing(filename: str, stop_word_removal: bool) -> pd.DataFrame:
    """
    Preprocess the tab-separated file.
    :param filename: Tab-separated file to process
    :param stop_word_removal: True if stop words should be removed, False if not
    """
    df = pd.read_csv(filename, sep='\t', names=['ground_truth', 'text1', 'text2'])
    # Lowercasing
    df['text1'] = df['text1'].map(str.lower)
    df['text2'] = df['text2'].map(str.lower)
    # Tokenizing
    df['text1'] = df['text1'].map(word_tokenize)
    df['text2'] = df['text2'].map(word_tokenize)
    # Stopword removal
    if stop_word_removal is True:
        df['text1'] = df['text1'].apply(lambda x: [word for word in x if word not in stop_words])
        df['text2'] = df['text2'].apply(lambda x: [word for word in x if word not in stop_words])
    return df


def tfidf_vectorizer(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the TF-IDF scores for sentences.
    :param df: Pandas DataFrame containing the sentences
    :return DataFrame with additional column 'predicted_scores'
    """
    # Deep copy to avoid changing the existing copy
    dataframe = df.copy(deep=True)
    # Concatenate words to sentences again
    # Needed for TfidfVectorizer()
    dataframe['text1'] = [' '.join(word) for word in dataframe['text1'].values]
    dataframe['text2'] = [' '.join(word) for word in dataframe['text2'].values]
    vectorizer = TfidfVectorizer()
    # Concatenate rows of text2 to text1
    concatenated_text = pd.concat([dataframe.text1, dataframe.text2])
    vectors = vectorizer.fit_transform(concatenated_text)
    predicted_scores = []
    for i in range(0, 249):
        # Calculate pairwise similarity score (text1, text2) for each row
        predicted_scores.append(cosine_similarity(vectors[i], vectors[i+249])[0][0])
    dataframe['predicted_scores'] = predicted_scores
    return dataframe

def short_vector_mean(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the similarity score of sentences using an average of the word embeddings.
    :param df: Pandas DataFrame containing the sentences
    :return DataFrame with additional column 'predicted_scores'
    """
    predicted_scores = []
    # Deep copy to avoid changing the existing copy
    dataframe = df.copy(deep=True)
    for i in range(0, 249):
        nwords = 0
        feature_vector1 = np.zeros((300,), dtype=np.float32)
        for word in dataframe.iloc[i].text1:
            # Iterate over words in first sentence
            if word in model:
                # Only add if word is in vocabulary
                nwords = nwords + 1
                feature_vector1 = np.add(feature_vector1, model.get_vector(word, norm=True))
        if nwords != 0:
            feature_vector1 = np.divide(feature_vector1, nwords)
        nwords = 0
        feature_vector2 = np.zeros((300,), dtype=np.float32)
        for word in dataframe.iloc[i].text2:
            # Iterate over words in second sentence
            if word in model:
                # Only add if word is in vocabulary
                nwords = nwords + 1
                feature_vector2 = np.add(feature_vector2, model.get_vector(word, norm=True))
        if nwords != 0:
            feature_vector2 = np.divide(feature_vector2, nwords)
        # Reshape the vectors so that we get only one score back
        predicted_scores.append(cosine_similarity(feature_vector1.reshape(1,-1), feature_vector2.reshape(1, -1))[0][0])
    dataframe['predicted_scores'] = predicted_scores
    return dataframe


def evaluate(df_simple: pd.DataFrame, df_full: pd.DataFrame):
    """
    Prints the pearson coefficient for a dataset with stop words and a second one without.
    Expects a 'predicted_scores' column per DataFrame.
    :param df_simple: Pandas DataFrame without stop words removed
    :param df_full: Pandas DataFrame with stop words removed
    """
    print(f'Simple preprocessing: {pearsonr(df_simple.ground_truth, df_simple.predicted_scores)}')
    print(f'Full preprocessing: {pearsonr(df_full.ground_truth, df_full.predicted_scores)}')
    print()

if __name__ == '__main__':
    df_0 = preprocessing('../dataset.tsv', False)
    df_1 = preprocessing('../dataset.tsv', True)

    df_tfidf_simple = tfidf_vectorizer(df_0)
    df_tfidf_full = tfidf_vectorizer(df_1)

    print('======== TfidfVectorizer ========')
    evaluate(df_tfidf_simple, df_tfidf_full)

    df_svm_simple = short_vector_mean(df_0)
    df_svm_full = short_vector_mean(df_1)

    print('======== Short Vector Mean ========')
    evaluate(df_svm_simple, df_svm_full)
