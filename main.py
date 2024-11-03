import pandas as pd
from sentence_transformers import SentenceTransformer
from src.utils import loss, check_embeddings
from src.autoencoder import AutoEncoder
from src.query import QuerySearch
import torch
import json

def main():
    # Step 1
    print("Step 1: Loading data and training the autoencoder")
    df: pd.DataFrame = pd.read_parquet("scrapper/output/compiled_pokemon.parquet")

    model = SentenceTransformer("all-MiniLM-L6-v2")

    print("Embedding descriptions...")
    embeddings = model.encode(df["description"].tolist(), convert_to_tensor=True)
    torch.save(embeddings, "outputs/embeddings.pt")

    print("Training the autoencoder...")
    autoencoder = AutoEncoder(input_dim=embeddings.shape[1], hidden_dim=128)

    print("Fine-tuning the autoencoder...")
    tuned_embedding = loss(autoencoder, embeddings)

    # Step 2
    print("Step 2: Checking the embeddings")
    check_embeddings(tuned_embedding, embeddings)

    torch.save(tuned_embedding, "outputs/tuned_embedding.pt")

    # Step 3
    print("Step 3: Querying the model")
    queries = ["A creature that worships the sun and lives in an active volcano. It likes fire and arson.", "Bakes cakes and serves pastries to friends", "A creature that bullies others and prefers to be alone. It is very strong and likes to fight and dislikes other people."]

    query_search = QuerySearch(model, autoencoder, tuned_embedding, df["description"].tolist(), df["name"].tolist())

    results = query_search.search(queries)

    for query, similar_descriptions in results.items():
        print(f"Query: {query}")
        print("Number of results: ", len(similar_descriptions))
        for name, desc, score in similar_descriptions:
            print(f"Pokemon: {name}, Description: {desc}, Score: {score}")
        print("\n ----- \n")

    # print("Saving results...")
    # with open("outputs/results.json", "w", encoding="utf-8") as f:
    #     for query, similar_descriptions in results.items():
    #         res = {query: [(str(len(similar_descriptions)), name, desc, str(score)) for name, desc, score in similar_descriptions]}
    #         json.dump(res, f, indent=4)
    

if __name__ == '__main__':
    main()
