import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class model:
    def __init__(self, df):
        self.df = df
        self.vectorizer = TfidfVectorizer()
        self.X = self.vectorizer.fit_transform(self.df['description'])
    
    def get_similar_cards(self, query):
        query_vec = self.vectorizer.transform([query])
        cosine_similarities = cosine_similarity(query_vec, self.X).flatten()
        top_indices = cosine_similarities.argsort()[-10:][::-1]
        similar_cards = self.df.iloc[top_indices]
        return similar_cards
