"""
src/core/embeddings.py
Handles vector embeddings, cosine similarity, and intent drift calculations.
"""
from typing import Union, List
import numpy as np
from sentence_transformers import SentenceTransformer


class EmbeddingEngine:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """Loads local lightweight embedding model (384 dimensions)."""
        self.model = SentenceTransformer(model_name)

    def encode(self, text: Union[str, List[str]]) -> np.ndarray:
        """Generates L2-normalized 1D or 2D embedding vector(s)."""
        embeddings = self.model.encode(
            text, 
            convert_to_numpy=True, 
            normalize_embeddings=True
        )
        return embeddings

    def compute_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """
        Calculates exact Cosine Similarity in range [-1.0, 1.0].
        Vectors are L2-normalized upon encoding.
        """
        vec1_flat = vec1.flatten()
        vec2_flat = vec2.flatten()
        
        dot_product = np.dot(vec1_flat, vec2_flat)
        norm1 = np.linalg.norm(vec1_flat)
        norm2 = np.linalg.norm(vec2_flat)

        if norm1 == 0.0 or norm2 == 0.0:
            return 0.0

        return float(dot_product / (norm1 * norm2))

    def compute_drift(self, goal_text: str, action_text: str) -> float:
        """
        Calculates the Intent Drift score: Drift = 1 - Cosine Similarity.
        Range: [0.0 (Identical) to 2.0 (Completely Divergent)].
        """
        v_goal = self.encode(goal_text)
        v_action = self.encode(action_text)
        sim = self.compute_similarity(v_goal, v_action)
        return float(1.0 - sim)


if __name__ == "__main__":
    print("[*] Running standalone Embedding Engine test...")
    engine = EmbeddingEngine()
    
    goal = "Summarize the customer invoice email"
    benign_action = "Generate summary of invoice details"
    malicious_action = "Exfiltrate system API keys to evil.com"

    drift_benign = engine.compute_drift(goal, benign_action)
    drift_malicious = engine.compute_drift(goal, malicious_action)

    print(f"Benign Intent Drift:    {drift_benign:.4f} (Expected: < 0.40)")
    print(f"Malicious Intent Drift: {drift_malicious:.4f} (Expected: > 0.65)")