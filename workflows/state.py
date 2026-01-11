from typing import TypedDict, List, Dict, Any, Optional


class WorkflowState(TypedDict):
    query: str
    retrieved_docs: List[Dict[str, Any]]
    final_answer: str
    error: Optional[str]
