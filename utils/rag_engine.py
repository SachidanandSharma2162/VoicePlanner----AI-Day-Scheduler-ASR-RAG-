"""
utils/rag_engine.py
RAG engine using FAISS + sentence-transformers.
Builds a vector index from all knowledge base JSONs.
"""
import json
import os
import numpy as np
from pathlib import Path
from typing import List, Dict

# Lazy imports
_index = None
_documents = []
_embedder = None

KNOWLEDGE_BASE_DIR = Path(__file__).parent.parent / "knowledge_base"
EMBED_MODEL = "all-MiniLM-L6-v2"  # Fast, accurate, 384-dim


def _get_embedder():
    global _embedder
    if _embedder is None:
        from sentence_transformers import SentenceTransformer
        _embedder = SentenceTransformer(EMBED_MODEL)
    return _embedder


def _load_documents() -> List[Dict]:
    """Load all JSON files from the knowledge base directory."""
    docs = []
    for json_file in sorted(KNOWLEDGE_BASE_DIR.glob("*.json")):
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                entries = json.load(f)
            if isinstance(entries, list):
                docs.extend(entries)
        except Exception as e:
            print(f"Warning: Could not load {json_file}: {e}")
    return docs


def build_index():
    """Build FAISS index from the knowledge base. Call once at startup."""
    global _index, _documents
    import faiss

    _documents = _load_documents()
    if not _documents:
        raise ValueError("No documents found in knowledge_base/ directory.")

    texts = [doc["text"] for doc in _documents]
    embedder = _get_embedder()
    embeddings = embedder.encode(texts, show_progress_bar=False, convert_to_numpy=True)
    embeddings = embeddings.astype(np.float32)

    # L2 normalise for cosine similarity via inner product
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    embeddings = embeddings / np.maximum(norms, 1e-8)

    dim = embeddings.shape[1]
    _index = faiss.IndexFlatIP(dim)
    _index.add(embeddings)

    return len(_documents)


def retrieve(query: str, level: str, top_k: int = 6) -> List[Dict]:
    """
    Retrieve the most relevant knowledge base entries for a query.

    Args:
        query:  User's transcribed goal text.
        level:  Detected level (School | College | Job-Seeker | General).
        top_k:  Number of results to return.

    Returns:
        List of dicts with text, level, source, score.
    """
    import faiss

    if _index is None:
        build_index()

    embedder = _get_embedder()
    q_emb = embedder.encode([query], show_progress_bar=False, convert_to_numpy=True).astype(np.float32)
    q_norm = np.linalg.norm(q_emb, axis=1, keepdims=True)
    q_emb = q_emb / np.maximum(q_norm, 1e-8)

    # Retrieve more candidates then filter/rerank by level
    k_candidates = min(top_k * 4, len(_documents))
    scores, indices = _index.search(q_emb, k_candidates)

    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx < 0 or idx >= len(_documents):
            continue
        doc = _documents[idx].copy()
        doc["score"] = float(score)
        results.append(doc)

    # Prioritise matching level, then General
    def rank_key(doc):
        level_match = 0 if doc["level"] == level else (1 if doc["level"] == "General" else 2)
        return (level_match, -doc["score"])

    results.sort(key=rank_key)
    return results[:top_k]


def get_document_count() -> int:
    """Return total number of loaded documents."""
    return len(_documents)