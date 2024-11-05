import torch
import torch.nn as nn
from tqdm import tqdm
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
from collections import Counter

def loss(model, embeddings):
    """
    Fine-tune the model using the embeddings.

    Args:
        model: The autoencoder model.
        embeddings: The embeddings to fine-tune the model.

    Returns:
        tuned_embeddings : The tuned embeddings.
    """    
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    loss_fn = nn.MSELoss()

    for epoch in tqdm(range(100)):
        optimizer.zero_grad()
        output = model(embeddings)
        loss = loss_fn(output, embeddings)
        loss.backward()
        optimizer.step()

    with torch.no_grad():
        tuned_embeddings = model.encoder(embeddings)

    return tuned_embeddings

def check_embeddings(tuned_model, model, descriptions, n_clusters=5):
    """
    Plot the embeddings and compare the clusters.

    Args:
        tuned_model : The tuned model.
        model : The original model.
        n_clusters (int, optional): Amount of clusters to be generated for k-means. Defaults to 5.
    """    
    tsne_og = TSNE(n_components=2, random_state=42)
    embeddings = tsne_og.fit_transform(model.cpu().numpy())

    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(embeddings)

    plt.figure(figsize=(5, 5))
    plt.scatter(embeddings[:, 0], embeddings[:, 1], c=clusters, cmap='viridis', alpha=0.5)
    
    plt.xlabel('Embedding Dimension 1')
    plt.ylabel('Embedding Dimension 2')
    plt.title('Scatter Plot of Model Embeddings with Clusters')
    plt.colorbar(label='Cluster Label')
    plt.grid(True)
    plt.savefig('outputs/embeddings.png')
    plt.show()

    original_cluster_analysis(clusters, descriptions, n_clusters)

    # Plot tuned embeddings

    tsne_tuned = TSNE(n_components=2, random_state=42)
    tuned_embeddings = tsne_tuned.fit_transform(tuned_model.cpu().numpy())

    tuned_clusters = kmeans.fit_predict(tuned_embeddings)

    plt.figure(figsize=(5, 5))
    plt.scatter(tuned_embeddings[:, 0], tuned_embeddings[:, 1], c=tuned_clusters, cmap='viridis', alpha=0.5)
    
    plt.xlabel('Embedding Dimension 1')
    plt.ylabel('Embedding Dimension 2')
    plt.title('Scatter Plot of Tuned Embeddings with Clusters')
    plt.colorbar(label='Cluster Label')
    plt.grid(True)
    plt.savefig('outputs/tuned_embeddings.png')
    plt.show()

    tuned_cluster_analysis(tuned_clusters, descriptions, n_clusters)


def original_cluster_analysis(clusters, descriptions, n_clusters):
    """
    Analyze the original clusters to identify the most common descriptions.

    Args:
        clusters: Array of cluster labels for the original embeddings.
        descriptions: List of descriptions corresponding to the embeddings.
        n_clusters: Number of clusters.
    """
    for cluster_id in range(n_clusters):
        cluster_descriptions = [descriptions[i] for i in range(len(descriptions)) if clusters[i] == cluster_id]
        if cluster_descriptions:
            most_common = Counter(cluster_descriptions).most_common(3)  # Top 3 common descriptions
            print(f'Cluster {cluster_id}: {most_common}')


def tuned_cluster_analysis(clusters, descriptions, n_clusters):
    """
    Analyze the tuned clusters to identify the most common descriptions.

    Args:
        clusters: Array of cluster labels for the tuned embeddings.
        descriptions: List of descriptions corresponding to the embeddings.
        n_clusters: Number of clusters.
    """
    for cluster_id in range(n_clusters):
        cluster_descriptions = [descriptions[i] for i in range(len(descriptions)) if clusters[i] == cluster_id]
        if cluster_descriptions:
            most_common = Counter(cluster_descriptions).most_common(3)  # Top 3 common descriptions
            print(f'Tuned Cluster {cluster_id}: {most_common}')