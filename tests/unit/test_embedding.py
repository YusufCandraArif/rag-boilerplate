from services.embedding import FastEmbedEmbeddingService


def test_embedding_dimension():
    service = FastEmbedEmbeddingService()
    vector = service.embed("hello world")

    assert isinstance(vector, list)
    assert len(vector) == service.dimension


def test_embedding_deterministic():
    service = FastEmbedEmbeddingService()

    v1 = service.embed("same text")
    v2 = service.embed("same text")

    assert v1 == v2
