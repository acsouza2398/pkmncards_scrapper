import numpy as np
import torch
from sklearn.metrics.pairwise import cosine_similarity

class QuerySearch:
    def __init__(self, original_model, autoencoder, tuned_embeddings, descriptions, names):
        """
        Initialize the QuerySearch class.

        Args:
            original_model: The SentenceTransformer model for queries.
            autoencoder: The trained autoencoder model for tuning.
            tuned_embeddings: The array of tuned embeddings.
            descriptions: A list of character descriptions corresponding to the tuned embeddings.
        """
        self.original_model = original_model
        self.autoencoder = autoencoder
        self.tuned_embeddings = tuned_embeddings
        self.descriptions = descriptions
        self.character_names = names

    def get_embeddings(self, queries):
        """
        Get embeddings for the list of queries using the original model.

        Args:
            queries: A list of strings representing the queries.

        Returns:
            A NumPy array of embeddings for the queries.
        """
        with torch.no_grad():
            embeddings = self.original_model.encode(queries, convert_to_tensor=True)
            return embeddings.cpu()

    def search(self, queries, top_k=10, threshold=0.99):
        """
        Search for the most similar descriptions based on queries.

        Args:
            queries: A list of strings representing the queries.
            top_k: Number of top similar results to return.
            threshold: Minimum score threshold to include a description.

        Returns:
            A dictionary with queries as keys and the top K similar descriptions along with their scores as values.
        """
        results = {}
        query_embeddings = self.get_embeddings(queries)
        
        # Get the encoded representations from the autoencoder
        query_embeddings_encoded = self.autoencoder.encode(query_embeddings)

        # Calculate similarities using the tuned embeddings
        similarities = cosine_similarity(query_embeddings_encoded.cpu().numpy(), self.tuned_embeddings.cpu().numpy())

        for i, query in enumerate(queries):
            # Get top indices based on similarity scores
            top_indices = np.argsort(similarities[i])[::-1][:top_k]
            
            # Create a list of (character name, description, score) tuples
            top_results = [
                (self.character_names[idx], self.descriptions[idx], similarities[i][idx])
                for idx in top_indices
            ]
            
            # Filter based on the threshold
            filtered_results = [(name, desc, score) for name, desc, score in top_results if score > threshold]
            
            results[query] = filtered_results

        # Filter out queries with no results
        results = {query: desc for query, desc in results.items() if desc}

        return results
