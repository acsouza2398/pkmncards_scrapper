import pandas as pd
from sentence_transformers import SentenceTransformer
from src.utils import loss, check_embeddings
from src.autoencoder import AutoEncoder
import torch

def main():
    df: pd.DataFrame = pd.read_parquet("scrapper/output/compiled_pokemon.parquet")

    model = SentenceTransformer("paraphrase-MiniLM-L6-v2")

    embeddings = model.encode(df["description"].tolist(), convert_to_tensor=True)
    torch.save(embeddings, "outputs/embeddings.pt")
    
    autoencoder = AutoEncoder(input_dim=embeddings.shape[1], hidden_dim=128)

    tuned_embedding = loss(autoencoder, embeddings)

    check_embeddings(tuned_embedding, embeddings)

    torch.save(tuned_embedding, "outputs/tuned_embedding.pt")

if __name__ == '__main__':
    main()
