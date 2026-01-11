# RAG Boilerplate

A production-oriented FastAPI service for document ingestion and semantic retrieval using Retrieval-Augmented Generation (RAG).

## Project Structure

```text
├── api
│   ├── routes.py
│   └── schemas.py
├── application
│   └── document_service.py
├── core
│   ├── config.py
│   ├── __init__.py
│   └── logging.py
├── entrypoint.sh
├── infrastructure
│   ├── __init__.py
│   └── lifespan.py
├── main.py
├── README.md
├── services
│   ├── embedding.py
│   ├── __init__.py
│   └── vector_store
│       ├── base.py
│       └── qdrant_store.py
├── tests
│   ├── integration
│   │   └── test_api.py
│   └── unit
│       ├── test_embedding.py
│       └── test_nodes.py
└── workflows
    ├── graph.py
    ├── __init__.py
    ├── nodes.py
    └── state.py
