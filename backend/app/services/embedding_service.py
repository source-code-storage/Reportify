"""
Embedding service for generating text embeddings using Sentence Transformers
"""

from typing import List, Optional, Tuple
import numpy as np


class EmbeddingService:
    """Service for generating text embeddings"""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize embedding service.

        Args:
            model_name: Name of the sentence transformer model
        """
        self.model_name = model_name
        self._model = None
        self._embedding_dim = 384  # Default for all-MiniLM-L6-v2

    @property
    def model(self):
        """Lazy load the model"""
        if self._model is None:
            try:
                from sentence_transformers import SentenceTransformer

                self._model = SentenceTransformer(self.model_name)
                self._embedding_dim = self._model.get_sentence_embedding_dimension()
            except ImportError:
                raise ImportError(
                    "sentence-transformers is required. Install with: pip install sentence-transformers"
                )
        return self._model

    @property
    def embedding_dimension(self) -> int:
        """Get the embedding dimension"""
        return self._embedding_dim

    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.

        Args:
            text: Text to embed

        Returns:
            List of floats representing the embedding
        """
        if not text or not text.strip():
            return [0.0] * self._embedding_dim

        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding.tolist()

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts.

        Args:
            texts: List of texts to embed

        Returns:
            List of embeddings
        """
        if not texts:
            return []

        # Filter empty texts
        valid_texts = [t if t and t.strip() else " " for t in texts]

        embeddings = self.model.encode(valid_texts, convert_to_numpy=True)
        return embeddings.tolist()

    def chunk_text(
        self, text: str, max_chunk_size: int = 500, overlap: int = 50
    ) -> List[Tuple[str, int]]:
        """
        Split text into chunks for embedding.

        Args:
            text: Text to chunk
            max_chunk_size: Maximum characters per chunk
            overlap: Number of characters to overlap between chunks

        Returns:
            List of (chunk_text, chunk_index) tuples
        """
        if not text or not text.strip():
            return []

        # Split by sentences first
        sentences = self._split_into_sentences(text)

        chunks = []
        current_chunk = []
        current_length = 0
        chunk_index = 0

        for sentence in sentences:
            sentence_length = len(sentence)

            if current_length + sentence_length > max_chunk_size and current_chunk:
                # Save current chunk
                chunk_text = " ".join(current_chunk)
                chunks.append((chunk_text, chunk_index))
                chunk_index += 1

                # Start new chunk with overlap
                if overlap > 0 and len(current_chunk) > 1:
                    # Keep last sentence(s) for overlap
                    overlap_text = current_chunk[-1]
                    current_chunk = [overlap_text]
                    current_length = len(overlap_text)
                else:
                    current_chunk = []
                    current_length = 0

            current_chunk.append(sentence)
            current_length += sentence_length + 1  # +1 for space

        # Don't forget the last chunk
        if current_chunk:
            chunk_text = " ".join(current_chunk)
            chunks.append((chunk_text, chunk_index))

        return chunks

    def _split_into_sentences(self, text: str) -> List[str]:
        """
        Split text into sentences.

        Args:
            text: Text to split

        Returns:
            List of sentences
        """
        import re

        # Simple sentence splitting
        # Split on period, exclamation, question mark followed by space or end
        sentences = re.split(r"(?<=[.!?])\s+", text)

        # Clean up
        sentences = [s.strip() for s in sentences if s.strip()]

        return sentences

    def compute_similarity(
        self, embedding1: List[float], embedding2: List[float]
    ) -> float:
        """
        Compute cosine similarity between two embeddings.

        Args:
            embedding1: First embedding
            embedding2: Second embedding

        Returns:
            Similarity score (0-1)
        """
        vec1 = np.array(embedding1)
        vec2 = np.array(embedding2)

        # Cosine similarity
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return float(dot_product / (norm1 * norm2))

    def find_most_similar(
        self,
        query_embedding: List[float],
        embeddings: List[List[float]],
        top_k: int = 5,
    ) -> List[Tuple[int, float]]:
        """
        Find most similar embeddings to a query.

        Args:
            query_embedding: Query embedding
            embeddings: List of embeddings to search
            top_k: Number of results to return

        Returns:
            List of (index, similarity_score) tuples
        """
        if not embeddings:
            return []

        similarities = []
        for i, emb in enumerate(embeddings):
            sim = self.compute_similarity(query_embedding, emb)
            similarities.append((i, sim))

        # Sort by similarity (descending)
        similarities.sort(key=lambda x: x[1], reverse=True)

        return similarities[:top_k]

    def process_note_for_embedding(
        self, text: str, max_chunk_size: int = 500, overlap: int = 50
    ) -> List[Tuple[str, List[float]]]:
        """
        Process a note text into chunks and generate embeddings.

        Args:
            text: Note text to process
            max_chunk_size: Maximum characters per chunk
            overlap: Number of characters to overlap between chunks

        Returns:
            List of (chunk_text, embedding) tuples
        """
        # Chunk the text
        chunks = self.chunk_text(text, max_chunk_size, overlap)

        if not chunks:
            return []

        # Extract just the text from chunks (ignore index)
        chunk_texts = [chunk_text for chunk_text, _ in chunks]

        # Generate embeddings for all chunks
        embeddings = self.generate_embeddings(chunk_texts)

        # Combine chunks with their embeddings
        return list(zip(chunk_texts, embeddings))


# Singleton instance
embedding_service = EmbeddingService()


# Global instance
_embedding_service = None


def get_embedding_service() -> EmbeddingService:
    """Get or create the global embedding service instance"""
    global _embedding_service
    if _embedding_service is None:
        _embedding_service = EmbeddingService()
    return _embedding_service
