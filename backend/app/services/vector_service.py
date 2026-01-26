"""
Vector Database Service
Handles storage and retrieval of embeddings using Qdrant
"""

from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue,
)
from qdrant_client.http import models
import uuid

from app.core.config import settings


class VectorService:
    """Service for vector database operations using Qdrant"""

    def __init__(self):
        """Initialize Qdrant client"""
        self.client = QdrantClient(url=settings.QDRANT_URL)
        self.collection_name = "note_embeddings"
        self.embedding_dim = 384  # Dimension for all-MiniLM-L6-v2

        # Create collection if it doesn't exist
        self._ensure_collection_exists()

    def _ensure_collection_exists(self):
        """Create the collection if it doesn't exist"""
        try:
            self.client.get_collection(self.collection_name)
        except Exception:
            # Collection doesn't exist, create it
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.embedding_dim, distance=Distance.COSINE
                ),
            )

    def store_embedding(
        self,
        embedding: List[float],
        note_id: int,
        chunk_index: int,
        chunk_text: str,
        report_id: int,
        user_id: int,
        filename: str,
        file_type: str,
    ) -> str:
        """
        Store a single embedding in Qdrant

        Args:
            embedding: The embedding vector
            note_id: Database ID of the note
            chunk_index: Index of this chunk within the note
            chunk_text: The actual text of this chunk
            report_id: ID of the report this note belongs to
            user_id: ID of the user who owns this note
            filename: Original filename
            file_type: Type of file (pdf, txt, etc.)

        Returns:
            UUID of the stored point in Qdrant
        """
        point_id = str(uuid.uuid4())

        point = PointStruct(
            id=point_id,
            vector=embedding,
            payload={
                "note_id": note_id,
                "chunk_index": chunk_index,
                "chunk_text": chunk_text,
                "report_id": report_id,
                "user_id": user_id,
                "filename": filename,
                "file_type": file_type,
            },
        )

        self.client.upsert(collection_name=self.collection_name, points=[point])

        return point_id

    def store_embeddings_batch(
        self,
        embeddings: List[List[float]],
        note_id: int,
        chunks: List[str],
        report_id: int,
        user_id: int,
        filename: str,
        file_type: str,
    ) -> List[str]:
        """
        Store multiple embeddings in batch (more efficient)

        Args:
            embeddings: List of embedding vectors
            note_id: Database ID of the note
            chunks: List of text chunks corresponding to embeddings
            report_id: ID of the report
            user_id: ID of the user
            filename: Original filename
            file_type: Type of file

        Returns:
            List of UUIDs for the stored points
        """
        points = []
        point_ids = []

        for idx, (embedding, chunk_text) in enumerate(zip(embeddings, chunks)):
            point_id = str(uuid.uuid4())
            point_ids.append(point_id)

            points.append(
                PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload={
                        "note_id": note_id,
                        "chunk_index": idx,
                        "chunk_text": chunk_text,
                        "report_id": report_id,
                        "user_id": user_id,
                        "filename": filename,
                        "file_type": file_type,
                    },
                )
            )

        self.client.upsert(collection_name=self.collection_name, points=points)

        return point_ids

    def search_similar(
        self,
        query_embedding: List[float],
        report_id: int,
        user_id: int,
        limit: int = 5,
        file_type_filter: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Search for similar embeddings

        Args:
            query_embedding: The query vector
            report_id: Filter by report ID
            user_id: Filter by user ID
            limit: Maximum number of results
            file_type_filter: Optional filter by file type

        Returns:
            List of search results with scores and metadata
        """
        # Build filter
        must_conditions = [
            FieldCondition(key="report_id", match=MatchValue(value=report_id)),
            FieldCondition(key="user_id", match=MatchValue(value=user_id)),
        ]

        if file_type_filter:
            must_conditions.append(
                FieldCondition(
                    key="file_type", match=MatchValue(value=file_type_filter)
                )
            )

        search_filter = Filter(must=must_conditions)

        # Perform search
        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_embedding,
            query_filter=search_filter,
            limit=limit,
        ).points

        # Format results
        formatted_results = []
        for result in results:
            formatted_results.append(
                {
                    "score": result.score,
                    "note_id": result.payload["note_id"],
                    "chunk_index": result.payload["chunk_index"],
                    "chunk_text": result.payload["chunk_text"],
                    "filename": result.payload["filename"],
                    "file_type": result.payload["file_type"],
                }
            )

        return formatted_results

    def delete_note_embeddings(self, note_id: int):
        """Delete all embeddings for a specific note"""
        self.client.delete(
            collection_name=self.collection_name,
            points_selector=models.FilterSelector(
                filter=Filter(
                    must=[
                        FieldCondition(key="note_id", match=MatchValue(value=note_id))
                    ]
                )
            ),
        )

    def delete_report_embeddings(self, report_id: int):
        """Delete all embeddings for a specific report"""
        self.client.delete(
            collection_name=self.collection_name,
            points_selector=models.FilterSelector(
                filter=Filter(
                    must=[
                        FieldCondition(
                            key="report_id", match=MatchValue(value=report_id)
                        )
                    ]
                )
            ),
        )


# Global instance
_vector_service = None


def get_vector_service() -> VectorService:
    """Get or create the global vector service instance"""
    global _vector_service
    if _vector_service is None:
        _vector_service = VectorService()
    return _vector_service
