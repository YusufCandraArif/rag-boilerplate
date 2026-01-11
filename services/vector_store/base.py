from abc import ABC, abstractmethod
from typing import List, Any
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings


class BaseVectorStore(ABC):
    """Abstract base class for vector store implementations"""

    @abstractmethod
    def __init__(self, collection_name: str, embedding_function: Embeddings, **kwargs):
        pass

    @abstractmethod
    def add_documents(self, documents: List[Document]) -> None:
        pass

    @abstractmethod
    def delete(self, ids: List[str]) -> None:
        pass

    @abstractmethod
    def as_retriever(self, **kwargs: Any):
        pass

    @abstractmethod
    def similarity_search(self, query: str, k: int = 4, **kwargs: Any) -> List[Document]:
        pass

    @abstractmethod
    def similarity_search_with_score(
        self, query: str, k: int = 4, **kwargs: Any
    ) -> List[Document]:
        pass

    @abstractmethod
    def delete_collection(self) -> None:
        pass

    @abstractmethod
    def get_collection_count(self) -> int:
        pass
