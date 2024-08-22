import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class model:
    """
    Model class to get the similar pokédex entries
    1. df: pd.DataFrame -> The dataframe to store the entries
    2. vectorizer: TfidfVectorizer -> The vectorizer to vectorize the text
    3. X: np.ndarray -> The vectorized text
    4. get_similar_entries(query: str) -> Get the similar entries
    """    
    def __init__(self, df):
        self.df: pd.DataFrame = df
        self.vectorizer: TfidfVectorizer = TfidfVectorizer()
        self.X: np.ndarray = self.vectorizer.fit_transform(self.df['description'])
    
    def get_similar_entries(self, query: str) -> pd.DataFrame:
        """
        Get the similar entries based on the query string
        1. Vectorize the query
        2. Calculate the cosine similarity
        3. Get the top 10 similar entries
        4. Return the similar entries

        Args:
            query (str): The query string from the user

        Returns:
            pd.DataFrame: The similar entries
        """        
        query_vec = self.vectorizer.transform([query])
        cosine_similarities = cosine_similarity(query_vec, self.X).flatten()
        top_indices = cosine_similarities.argsort()[-10:][::-1]
        
        similar_entries = self.df.iloc[top_indices].copy()
        similar_entries["score"] = cosine_similarities[top_indices]
        
        similar_entries = similar_entries[similar_entries['score'] > 0.11]
        return similar_entries

