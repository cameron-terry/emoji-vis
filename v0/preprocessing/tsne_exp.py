import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE


def find_optimal_pca_components(embeddings, variance_threshold=0.95):
    # Apply PCA without specifying the number of components to capture all variance
    pca = PCA().fit(embeddings)
    cumulative_variance = np.cumsum(pca.explained_variance_ratio_)

    # Plot cumulative explained variance to visualize the "elbow"
    plt.plot(cumulative_variance)
    plt.xlabel("Number of Components")
    plt.ylabel("Cumulative Explained Variance")
    plt.title("Explained Variance vs. Number of Components")
    plt.grid()
    plt.show()

    # Find the number of components needed to reach the variance threshold
    optimal_components = np.argmax(cumulative_variance >= variance_threshold) + 1
    print(
        f"Optimal number of components to retain {variance_threshold*100:.0f}% variance: {optimal_components}"
    )

    return optimal_components


def fit(embeddings, random_state=42):
    optimal_components = find_optimal_pca_components(embeddings)

    pca = PCA(n_components=optimal_components, random_state=random_state)
    tsne = TSNE(n_components=2, random_state=random_state, perplexity=30, max_iter=1000)

    embeddings_reduced = pca.fit_transform(embeddings)
    embeddings_2d = tsne.fit_transform(embeddings_reduced)

    return embeddings_2d
