import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize

class model:
    def __init__(self, df):
        self.df = df
        self.vectorizer = TfidfVectorizer()
        self.X = self.vectorizer.fit_transform(self.df['text'])
        self.similarity_matrix = self.X @ self.X.T
        self.similarity_matrix_dense = self.similarity_matrix.toarray()
    
    def get_similar_cards(self, query):
        similarity_scores = self.similarity_matrix_dense[self.df[self.df["text"].str.contains(query, case=False)].index]
        top_indices = similarity_scores.argsort()[-10:][::-1]
        top_indices = [i for i in top_indices]
        similar_cards = self.df.iloc[top_indices]
        return similar_cards
