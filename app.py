import streamlit as st
import mlflow.pyfunc
import pandas as pd
import torch
from sentence_transformers import SentenceTransformer
from src.query import QuerySearch
from src.autoencoder import AutoEncoder

@st.cache_resource
def load_production_model():
    # Get the latest run in the experiment
    experiment_name = "Default"  # Replace with your experiment name
    client = mlflow.tracking.MlflowClient()
    experiment_id = client.get_experiment_by_name(experiment_name).experiment_id
    latest_run = client.search_runs(experiment_id, order_by=["start_time DESC"], max_results=1)[0]

    # load autoencoder model
    autoencoder_path = f"mlruns/0/{latest_run.info.run_id}/artifacts/models/autoencoder"
    autoencoder = mlflow.pytorch.load_model(autoencoder_path)
    
    embeddings_path = f"mlruns/0/{latest_run.info.run_id}/artifacts/tuned_embeddings/tuned_embedding.pt"
    tuned_embeddings = torch.load(mlflow.artifacts.download_artifacts(embeddings_path))
    
    return autoencoder, tuned_embeddings

def main():
    st.title("Pokemon Character Query Search")

    original_model = SentenceTransformer("all-MiniLM-L6-v2")

    # Load models and embeddings
    autoencoder, tuned_embeddings = load_production_model()

    df: pd.DataFrame = pd.read_parquet("scrapper/output/compiled_pokemon.parquet")

    # Initialize the query search object
    query_search = QuerySearch(original_model, autoencoder, tuned_embeddings, df["description"].tolist(), df["name"].tolist())

    # Get user input for queries
    queries = st.text_area("Enter your queries (one per line)", "A creature that worships the sun and lives in an active volcano.\nBakes cakes and serves pastries to friends")
    queries_list = queries.strip().split("\n")

    if st.button("Search"):
        results = query_search.search(queries_list)

        if len(queries_list) == 0:
            st.write("Please enter at least one query.")
            return

        if len(results) == 0:
            st.write("No results found.")
            return

        c = st.columns(len(queries_list))  # Create columns

        for i, (query, similar_descriptions) in enumerate(results.items()):
            with c[i]:  # Access the correct column using the `cols` list
                st.write(f"Query: {query}")
                st.write("Number of results: ", len(similar_descriptions))
                for name, desc, score in similar_descriptions:
                    st.write(f"Pokemon: {name}, Description: {desc}, Score: {round(score, 3)}")
                st.write("\n ----- \n")

if __name__ == "__main__":
    main()