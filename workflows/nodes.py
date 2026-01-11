from typing import Dict, Any
from langchain_core.documents import Document
from workflows.state import WorkflowState
from services.vector_store.qdrant_store import QdrantStore


def retrieve_documents_node(
    state: WorkflowState,
    vector_store: QdrantStore,
    top_k: int = 5,
) -> WorkflowState:
    try:
        results = vector_store.similarity_search_with_score(
            state["query"], k=top_k
        )

        docs = []
        for doc, score in results:
            docs.append(
                {
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "score": score,
                }
            )

        state["retrieved_docs"] = docs
        state["error"] = None

    except Exception as e:
        state["error"] = str(e)
        state["retrieved_docs"] = []

    return state


def generate_answer_node(state: WorkflowState) -> WorkflowState:
    if state.get("error"):
        state["final_answer"] = f"Error: {state['error']}"
        return state

    if not state["retrieved_docs"]:
        state["final_answer"] = "No relevant documents found."
        return state

    top_doc = state["retrieved_docs"][0]["content"]
    state["final_answer"] = f"Based on the document: {top_doc[:200]}..."

    return state
