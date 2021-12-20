import pandas as pd
import gensim
import os
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.stats.stats import pearsonr

stop_words = set(stopwords.words('english'))
model_file = os.path.join('..', 'dataset', 'wiki-news-300d-1M-subword.vec')

def preprocessing(filename: str, stop_word_removal: bool) -> pd.DataFrame:
    """
    Preprocess the tab-separated file.
    :param filename: Tab-separated file to process
    :param stop_word_removal: True if stop words should be removed, False if not
    """
    df = pd.read_csv(filename, sep='\t', names=['ground_truth', 'text1', 'text2'])
    # lowercasing
    df['text1'] = df['text1'].map(str.lower)
    df['text2'] = df['text2'].map(str.lower)
    # tokenizing
    df['text1'] = df['text1'].map(word_tokenize)
    df['text2'] = df['text2'].map(word_tokenize)
    # stopword removal
    if stop_word_removal is True:
        df['text1'] = df['text1'].apply(lambda x: [word for word in x if word not in stop_words])
        df['text2'] = df['text2'].apply(lambda x: [word for word in x if word not in stop_words])
    # concatenate words to sentences again
    df['text1'] = [' '.join(word) for word in df['text1'].values]
    df['text2'] = [' '.join(word) for word in df['text2'].values]
    return df


def tfidf_vectorizer(df: pd.DataFrame) -> pd.DataFrame:
    vectorizer = TfidfVectorizer()
    # concatenate rows of text2 to text1
    concatenated_text = pd.concat([df.text1, df.text2])
    vectors = vectorizer.fit_transform(concatenated_text)
    predicted_scores = []
    for i in range(0, 249):
        # calculate pairwise similarity score (text1, text2) for each row
        predicted_scores.append(cosine_similarity(vectors[i], vectors[i+249])[0][0])
    df['predicted_scores'] = predicted_scores
    return df

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
