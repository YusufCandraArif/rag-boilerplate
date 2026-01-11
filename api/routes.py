import uuid
import time
from datetime import datetime
from typing import List

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
)

from langchain_core.documents import Document

from api.schemas import (
    DocumentInput,
    QueryInput,
    WorkflowResult,
)
from services.vector_store.qdrant_store import QdrantStore


router = APIRouter()

def get_vector_store(request: Request) -> QdrantStore:
    vector_store = getattr(request.app.state, "vector_store", None)
    if vector_store is None:
        raise HTTPException(
            status_code=500,
            detail="Vector store not initialized"
        )
    return vector_store


def get_workflow(request: Request):
    workflow = getattr(request.app.state, "workflow", None)
    if workflow is None:
        raise HTTPException(
            status_code=500,
            detail="Workflow not initialized"
        )
    return workflow


@router.post("/ingest")
def ingest_document(
    doc: DocumentInput,
    vector_store: QdrantStore = Depends(get_vector_store),
):
    document = Document(
        page_content=doc.content,
        metadata={
            **(doc.metadata or {}),
            "ingested_at": datetime.utcnow().isoformat(),
        },
    )

    vector_store.add_documents([document])

    return {
        "id": str(uuid.uuid4()),
        "message": "Document ingested successfully",
    }


@router.post("/batch_ingest")
def batch_ingest(
    documents: List[DocumentInput],
    vector_store: QdrantStore = Depends(get_vector_store),
):
    docs = [
        Document(
            page_content=doc.content,
            metadata={
                **(doc.metadata or {}),
                "ingested_at": datetime.utcnow().isoformat(),
            },
        )
        for doc in documents
    ]

    vector_store.add_documents(docs)

    return {
        "count": len(docs),
        "status": "success",
    }


@router.post("/query", response_model=WorkflowResult)
def query_documents(
    query_input: QueryInput,
    workflow = Depends(get_workflow),
):
    start_time = time.time()

    initial_state = {
        "query": query_input.query,
        "retrieved_docs": [],
        "final_answer": "",
        "error": None,
    }

    final_state = workflow.invoke(initial_state)

    return WorkflowResult(
        initial_query=query_input.query,
        retrieved_docs=final_state["retrieved_docs"],
        final_answer=final_state["final_answer"],
        processing_time=time.time() - start_time,
    )


@router.get("/documents")
def list_documents(
    limit: int = 10,
    vector_store: QdrantStore = Depends(get_vector_store),
):
    retriever = vector_store.as_retriever(
        search_kwargs={"k": limit}
    )

    docs = retriever.get_relevant_documents("")

    return {
        "documents": [
            {
                "content": d.page_content[:100] + "...",
                "metadata": d.metadata,
            }
            for d in docs
        ]
    }


@router.delete("/documents/{doc_id}")
def delete_document(
    doc_id: str,
    vector_store: QdrantStore = Depends(get_vector_store),
):
    vector_store.delete([doc_id])

    return {
        "message": f"Document {doc_id} deleted"
    }


@router.get("/health")
def health_check(
    vector_store: QdrantStore = Depends(get_vector_store),
    workflow = Depends(get_workflow),
):
    return {
        "status": "healthy",
        "documents": vector_store.get_collection_count(),
        "workflow": "ready",
    }


@router.get("/chaos")
async def chaos_mode():
    import asyncio
    import random

    await asyncio.sleep(random.uniform(0.1, 2.0))
    return {
        "message": "Chaos mode activated!",
        "random_number": random.randint(1, 100),
    }


_counter = 0

@router.get("/counter")
def get_counter():
    global _counter
    _counter += 1
    return {"counter": _counter}
