import umap


def fit(embeddings, n_neighbors=15, min_dist=0.1):
    reducer = umap.UMAP(
        n_neighbors=n_neighbors, min_dist=min_dist, n_components=2, random_state=42
    )
    embeddings_2d = reducer.fit_transform(embeddings)
    return embeddings_2d
