from typing import List, Any
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

from core.config import settings
from .base import BaseVectorStore


class QdrantStore(BaseVectorStore):
    """Qdrant vector store implementation"""

    def __init__(self, collection_name: str, embedding_function: Embeddings, **kwargs):
        self.collection_name = collection_name

        self.client = QdrantClient(
            url=settings.QDRANT_URL
        )

        self._store = QdrantVectorStore(
            client=self.client,
            collection_name=collection_name,
            embedding=embedding_function,
        )

    def add_documents(self, documents: List[Document]) -> None:
        self._store.add_documents(documents)

    def delete(self, ids: List[str]) -> None:
        self._store.delete(ids)

    def as_retriever(self, **kwargs: Any):
        return self._store.as_retriever(**kwargs)

    def similarity_search(
        self, query: str, k: int = 4, **kwargs: Any
    ) -> List[Document]:
        return self._store.similarity_search(query, k=k, **kwargs)

    def similarity_search_with_score(
        self, query: str, k: int = 4, **kwargs: Any
    ):
        return self._store.similarity_search_with_score(query, k=k, **kwargs)

    def delete_collection(self) -> None:
        self.client.delete_collection(self.collection_name)

    def get_collection_count(self) -> int:
        try:
            info = self.client.get_collection(self.collection_name)
            return info.points_count or 0
        except Exception:
            return 0
