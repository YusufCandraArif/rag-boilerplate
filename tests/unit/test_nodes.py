from workflows.nodes import generate_answer_node


def test_generate_answer_with_docs():
    state = {
        "query": "test",
        "retrieved_docs": [
            {"content": "This is a test document"}
        ],
        "final_answer": "",
        "error": None,
    }

    result = generate_answer_node(state)

    assert "Based on the document" in result["final_answer"]


def test_generate_answer_no_docs():
    state = {
        "query": "test",
        "retrieved_docs": [],
        "final_answer": "",
        "error": None,
    }

    result = generate_answer_node(state)

    assert result["final_answer"] == "No relevant documents found."
