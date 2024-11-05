import pandas as pd
from sentence_transformers import SentenceTransformer
from src.utils import loss, check_embeddings
from src.autoencoder import AutoEncoder
from src.query import QuerySearch
import torch
import json
import mlflow
import mlflow.pytorch

def main():
    # Start an MLflow run
    with mlflow.start_run() as run:
        
        # Step 1: Load data and train autoencoder
        print("Step 1: Loading data and training the autoencoder")
        df: pd.DataFrame = pd.read_parquet("scrapper/output/compiled_pokemon.parquet")

        model = SentenceTransformer("all-MiniLM-L6-v2")
        
        print("Embedding descriptions...")
        embeddings = model.encode(df["description"].tolist(), convert_to_tensor=True)
        torch.save(embeddings, "outputs/embeddings.pt")
        
        # Log SentenceTransformer embeddings
        mlflow.log_artifact("outputs/embeddings.pt", artifact_path="embeddings")
        
        print("Training the autoencoder...")
        autoencoder = AutoEncoder(input_dim=embeddings.shape[1], hidden_dim=128)

        print("Fine-tuning the autoencoder...")
        tuned_embedding = loss(autoencoder, embeddings)
        
        # Log the autoencoder model and embeddings
        mlflow.pytorch.log_model(autoencoder, artifact_path="models/autoencoder")
        torch.save(tuned_embedding, "outputs/tuned_embedding.pt")
        mlflow.log_artifact("outputs/tuned_embedding.pt", artifact_path="tuned_embeddings")

        # Step 2: Check embeddings
        print("Step 2: Checking the embeddings")
        check_embeddings(tuned_embedding, embeddings, df["description"].tolist())

        # Step 3: Query the model
        print("Step 3: Querying the model")
        queries = [
            "A creature that worships the sun and lives in an active volcano. It likes fire and arson.",
            "Bakes cakes and serves pastries to friends",
            "Psychic powers to destroy the world"
        ]

        query_search = QuerySearch(model, autoencoder, tuned_embedding, df["description"].tolist(), df["name"].tolist())
        results = query_search.search(queries)

        for query, similar_descriptions in results.items():
            print(f"Query: {query}")
            print("Number of results: ", len(similar_descriptions))
            for name, desc, score in similar_descriptions:
                print(f"Pokemon: {name}, Description: {desc}, Score: {score}")
            print("\n ----- \n")
        
        # Optional: Save and log query results
        results_file = "outputs/results.json"
        with open(results_file, "w", encoding="utf-8") as f:
            json_results = {
                query: [(name, desc, float(score)) for name, desc, score in similar_descriptions]
                for query, similar_descriptions in results.items()
            }
            json.dump(json_results, f, indent=4)
        
        mlflow.log_artifact(results_file, artifact_path="results")

if __name__ == '__main__':
    main()
