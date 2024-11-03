import torch
import torch.nn as nn
from tqdm import tqdm
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans

def loss(model, embeddings):
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    loss_fn = nn.MSELoss()

    for epoch in tqdm(range(50)):
        optimizer.zero_grad()
        output = model(embeddings)
        loss = loss_fn(output, embeddings)
        loss.backward()
        optimizer.step()

    with torch.no_grad():
        tuned_embeddings = model.encoder(embeddings)

    return tuned_embeddings

def check_embeddings(tuned_model, model, n_clusters=5):
    tsne_pre = TSNE(n_components=2, random_state=42)
    embeddings = tsne_pre.fit_transform(model.cpu().numpy())

    tsne_tuned = TSNE(n_components=2, random_state=42)
    tuned_embeddings = tsne_tuned.fit_transform(tuned_model.cpu().numpy())

    print("Original Embeddings Shape:", embeddings.shape)
    print("Tuned Embeddings Shape:", tuned_embeddings.shape)

    print("Unique points in Original Embeddings:", len(set([tuple(point) for point in embeddings])))
    print("Unique points in Tuned Embeddings:", len(set([tuple(point) for point in tuned_embeddings])))

    # Perform K-means clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(embeddings)

    # Create a scatter plot of the embeddings with clusters
    plt.figure(figsize=(5, 5))
    plt.scatter(embeddings[:, 0], embeddings[:, 1], c=clusters, cmap='viridis', alpha=0.5)
    
    plt.xlabel('Embedding Dimension 1')
    plt.ylabel('Embedding Dimension 2')
    plt.title('Scatter Plot of Model Embeddings with Clusters')
    plt.colorbar(label='Cluster Label')
    plt.grid(True)
    plt.savefig('outputs/embeddings.png')
    plt.show()

    # Perform K-means clustering on tuned embeddings
    tuned_clusters = kmeans.fit_predict(tuned_embeddings)

    # Create a scatter plot of the tuned embeddings with clusters
    plt.figure(figsize=(5, 5))
    plt.scatter(tuned_embeddings[:, 0], tuned_embeddings[:, 1], c=tuned_clusters, cmap='viridis', alpha=0.5)
    
    plt.xlabel('Embedding Dimension 1')
    plt.ylabel('Embedding Dimension 2')
    plt.title('Scatter Plot of Tuned Embeddings with Clusters')
    plt.colorbar(label='Cluster Label')
    plt.grid(True)
    plt.savefig('outputs/tuned_embeddings.png')
    plt.show()