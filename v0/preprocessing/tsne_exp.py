from sklearn.manifold import TSNE


def fit(embeddings):
    # Initialize t-SNE with desired parameters
    tsne = TSNE(n_components=2, random_state=42, perplexity=30, max_iter=1000)

    # Apply t-SNE to the embeddings
    embeddings_2d = tsne.fit_transform(embeddings)

    return embeddings_2d
