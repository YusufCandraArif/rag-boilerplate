# app/application/document_service.py

import uuid
import time
from datetime import datetime
from typing import Dict, Any, List

from services.embedding import EmbeddingService
from services.vector_store import VectorStore
from workflows.graph import build_workflow


class DocumentService:
    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_store: VectorStore,
    ):
        self.embedding = embedding_service
        self.vector_store = vector_store
        self.workflow = build_workflow()

    def ingest(self, content: str, metadata: Dict[str, Any] | None = None) -> str:
        vector = self.embedding.embed(content)
        doc_id = str(uuid.uuid4())

        payload = {
            "content": content,
            "metadata": metadata or {},
            "ingested_at": datetime.utcnow().isoformat(),
        }

        self.vector_store.upsert(
            doc_id=doc_id,
            vector=vector,
            payload=payload,
        )

        return doc_id

    def query(self, query: str, top_k: int = 5) -> Dict[str, Any]:
        start = time.time()

        state = {
            "query": query,
            "top_k": top_k,
        }

        result = self.workflow.invoke(state)

        return {
            "initial_query": query,
            "retrieved_docs": result.get("retrieved_docs", []),
            "final_answer": result.get("final_answer", ""),
            "processing_time": time.time() - start,
        }
