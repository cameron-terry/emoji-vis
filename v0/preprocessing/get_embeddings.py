from dotenv import load_dotenv
from huggingface_hub import InferenceClient
import os
import numpy as np

load_dotenv()


class Embedder:
    def __init__(self):
        self.hf_token = os.getenv("HF_INFERENCE_TOKEN")
        assert self.hf_token, "Please set the HF_INFERENCE_TOKEN environment variable"
        self.client = InferenceClient(token=self.hf_token)

    def get_embeddings(self, text: str, method: str = "mean") -> np.ndarray:
        emb = self.client.feature_extraction(text)
        fse = self.fixed_size_embeddings(emb, method)
        return fse

    def fixed_size_embeddings(self, emb: np.ndarray, method: str) -> np.ndarray:
        # CLS token embedding
        if method == "cls":
            return emb[0, 0, :]
        # Average of all token embeddings
        elif method == "mean":
            return np.mean(emb, axis=1)
        # max pooling
        elif method == "max":
            return np.max(emb, axis=1)

    def cosine_similarity(self, emb1: np.ndarray, emb2: np.ndarray) -> float:
        assert emb1.shape == emb2.shape, "Embeddings must have the same shape"

        # Remove the leading singleton dimension
        a = emb1.reshape(-1, emb1.shape[-1])  # Reshape to (n, d)
        b = emb2.reshape(-1, emb2.shape[-1])  # Reshape to (n, d)

        # Calculate cosine similarity for each pair of corresponding vectors
        cosine_similarities = np.array(
            [
                np.dot(a[i], b[i]) / (np.linalg.norm(a[i]) * np.linalg.norm(b[i]))
                for i in range(min(a.shape[0], b.shape[0]))
            ]
        )

        return cosine_similarities
