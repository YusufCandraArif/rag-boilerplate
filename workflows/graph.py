from langgraph.graph import StateGraph, END
from workflows.state import WorkflowState
from workflows.nodes import (retrieve_documents_node,generate_answer_node,
)
from services.vector_store.qdrant_store import QdrantStore


def build_workflow(vector_store: QdrantStore):
    graph = StateGraph(WorkflowState)

    graph.add_node(
        "retrieve",
        lambda state: retrieve_documents_node(state, vector_store),
    )
    graph.add_node("generate", generate_answer_node)

    graph.set_entry_point("retrieve")
    graph.add_edge("retrieve", "generate")
    graph.add_edge("generate", END)

    return graph.compile()
