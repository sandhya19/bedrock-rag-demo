# bedrock-rag-demo

🚀 **End-to-End RAG System with Hybrid Retrieval, Evaluation, Query Rewriting, and LLM Answer Generation**

An end-to-end solution for building Retrieval-Augmented Generation (RAG) workflows. This project demonstrates how to leverage Amazon Bedrock for AI-powered embeddings and PostgreSQL with pgvector for efficient semantic similarity search, enabling high-performance Q&A services.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [How It Works](#how-it-works)
- [Implemented Features](#implemented-features)
- [Retrieval Evaluation and Calibration](#retrieval-evaluation-and-calibration)
- [Query Rewriting Layer](#query-rewriting-layer)
- [What This Project Demonstrates](#what-this-project-demonstrates)
- [Future Improvements](#future-improvements)
- [License](#license)

---

## Overview

Demonstrates a full Retrieval-Augmented Generation (RAG) workflow including hybrid retrieval, evaluation, query rewriting, and grounded LLM answer generation.

- 🔍 **Scrapes** the Amazon Bedrock FAQ page
- 📝 **Chunks** each FAQ into structured Q&A pairs
- 🧠 **Generates embeddings** using Amazon Bedrock's embedding models
- 💾 **Stores** embeddings in PostgreSQL with pgvector extension
- 🔎 **Performs semantic search** to retrieve relevant FAQs based on user queries

This project focuses on retrieval architecture design and ranking calibration rather than only LLM integration. This showcases a production-style ingestion and retrieval pipeline suitable for enterprise applications.

---

## Architecture

### Ingestion Pipeline
```
FAQ Data → Chunking → Embedding Generation → Vector Storage (pgvector)
```

### Retrieval Pipeline
```
User Query 
→ Query Rewriting 
→ Hybrid Retrieval (Sematic + Keyword) 
→ Context Construction
→ LLM Generation (Amazon Bedrock)
→ Final Answer
```

---

## Tech Stack

| Category | Technology |
|----------|------------|
| **Language** | Python 3.9+ |
| **AI/ML** | Amazon Bedrock(Embeddings) |
| **Database** | PostgreSQL with pgvector |
| **Web Scraping** | BeautifulSoup |
| **Database Driver** | psycopg2 |
| **Containerization** | Docker |

---

## Project Structure

```
bedrock-rag-demo/
├── scraper/
│   ├── scrape_bedrock_faq.py       # Scrapes Bedrock FAQ page
│   └── bedrock_faq.json             # Raw FAQ data
├── ingestion/
│   ├── chunk_and_prepare.py         # Chunks FAQs into Q&A pairs
│   ├── embed_all_chunks.py          # Generates embeddings via Bedrock
│   ├── test_embedding.py            # Tests embedding access
│   ├── bedrock_chunks.json          # Chunked FAQ data
│   └── bedrock_chunks_with_embeddings.json  # Chunks with embeddings
├── storage/
│   └── load_into_pgvector.py        # Loads data into PostgreSQL
├── retrieval/
│   └── query_service.py             # Semantic search query service
├── requirements.txt                 # Python dependencies
└── README.md                        # This file
```

---

## Prerequisites

Before you begin, ensure you have the following installed and configured:

- **Python 3.9 or higher** - [Install Python](https://www.python.org/downloads/)
- **AWS CLI** - [Configure AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- **Bedrock model access** - Enable access to embedding models in your AWS account
- **Docker** - [Install Docker](https://docs.docker.com/get-docker/)

---

## Quick Start

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

**requirements.txt contains:**
```
boto3
requests
beautifulsoup4
psycopg2-binary
```

### Step 2: Scrape Amazon Bedrock FAQ

```bash
python scraper/scrape_bedrock_faq.py
```

**Output:** `scraper/bedrock_faq.json`

### Step 3: Prepare Q&A Chunks

```bash
python ingestion/chunk_and_prepare.py
```

**Output:** `ingestion/bedrock_chunks.json`

Each chunk contains:
- `id` - Unique identifier
- `question` - FAQ question
- `answer` - FAQ answer
- `combined_text` - Concatenated question and answer

### Step 4: Generate Embeddings with Bedrock

First, test your embedding access:

```bash
python ingestion/test_embedding.py
```

Then, generate embeddings for all chunks:

```bash
python ingestion/embed_all_chunks.py
```

**Output:** `ingestion/bedrock_chunks_with_embeddings.json`

### Step 5: Start PostgreSQL with pgvector

```bash
docker run -d \
  --name pgvector-demo \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 \
  ankane/pgvector
```

Verify the container is running:

```bash
docker ps
```

### Step 6: Create Database Table

Connect to the PostgreSQL container:

```bash
docker exec -it pgvector-demo psql -U postgres
```

Inside PostgreSQL, create the vector extension and table:

```sql
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE bedrock_faq (
  id TEXT PRIMARY KEY,
  question TEXT,
  answer TEXT,
  embedding VECTOR(1536)
);
```

Exit with `\q`

### Step 7: Load Data into Database

```bash
python storage/load_into_pgvector.py
```

**Expected output:**
```
Data inserted successfully.
```

### Step 8: Run Semantic Search

```bash
python retrieval/query_service.py
```

Try asking questions like:
- "What is Amazon Bedrock?"
- "How much does Amazon Bedrock cost?"
- "Which models are supported?"

The system will:
- 🔄 Generate an embedding for your query
- 🔍 Perform vector similarity search
- 📊 Return the top matching FAQ entries

### Run Full RAG Pipeline

```bash
python app.py
```

---

## How It Works

### Retrieval Strategy

This system combines multiple ranking signals:

1. Semantic similarity using Amazon Bedrock embeddings
2. Keyword relevance using PostgreSQL full text search
3. Weighted ranking prioritizing question fields
4. Exact match boosting for deterministic ranking
5. Scores from semantic and lexical retrieval are normalized and combined using weighted ranking to improve result stability and precision.

### Similarity Search Mechanism

The query embedding is compared against stored embeddings using the pgvector distance operator:

```sql
embedding <-> query_vector
```

**Lower distance values indicate higher similarity.** The system returns the FAQs with the smallest distances to your query, meaning they are semantically most similar.

### Example Workflow

1. User asks: "What can I use Bedrock for?"
2. System generates an embedding for this query
3. pgvector compares it against all stored FAQ embeddings
4. Returns the top-matched FAQ answers based on semantic similarity
5. User receives relevant information from the knowledge base

---

## Implemented Features

- Semantic search using Amazon Bedrock embeddings
- Vector similarity search with pgvector
- Keyword search using PostgreSQL full text search
- Weighted field ranking for question and answer
- Hybrid retrieval combining semantic and lexical signals
- Exact match boosting and score normalization
- Lightweight query rewriting for improving retrieval robustness
- Grounded LLM answer generation using Amazon Bedrock

---

## Retrieval Evaluation and Calibration

To validate ranking quality, a lightweight evaluation framework was added:

- Precision@1 measurement
- Precision@3 measurement
- Average latency tracking
- Misranking diagnostics

This allowed iterative tuning of hybrid ranking weights and heuristic boosts.

Through calibration, Precision@1 improved from ~0.6–0.7 to ~0.9 on structured test queries.

This demonstrates how retrieval quality depends not only on embeddings, but also on ranking design and query structure.

---

## Query Rewriting Layer

To improve retrieval robustness for short or ambiguous queries, a lightweight deterministic query rewriting layer was introduced.

The rewriting layer:

- Expands underspecified queries into structured question format
- Aligns user intent with indexed FAQ structure
- Handles common synonym gaps (e.g., pricing → cost)
- Preserves low latency and avoids additional model calls

## LLM Answer Generation

The system now includes a full Retrieval-Augmented Generation (RAG) pipeline.

After hybrid retrieval, the top ranked chunks are:

- Structured into contextual sources
- Injected into a grounded prompt
- Passed to an Amazon Bedrock foundation model
- Used to generate a final synthesized answer

The model is instructed to use only retrieved context and avoid hallucination.

This completes the end-to-end RAG workflow.

### Example Transformations

| Original Query | Rewritten Query |
|---------------|-----------------|
| Amazon Bedrock? | What is Amazon Bedrock? |
| Amazon Bedrock pricing? | What does Amazon Bedrock cost? |

### Impact

After introducing query rewriting:

- Precision@1 improved from ~0.7 to 1.0 on structured test queries
- Precision@3 improved from ~0.8 to 1.0
- Average latency remained stable

This demonstrates that retrieval quality often depends more on query normalization than on model complexity.

---

## What This Project Demonstrates

- End-to-end embedding pipeline design
- Vector database integration using pgvector
- Hybrid search architecture combining semantic and lexical retrieval
- Ranking calibration and score normalization
- Practical retrieval system tuning beyond basic RAG

---

## Future Improvements

- [ ] **Reranking Layer** - Improve result relevance with cross-encoders
- [ ] **LLM Answer Generation** - Generate answers instead of returning raw FAQs
- [ ] **FastAPI Endpoint** - Expose functionality via REST API
- [x] **Basic Retrieval Evaluation** - Precision@1, Precision@3, latency tracking
- [ ] **Advanced Evaluation & Logging** - Add structured metrics and ranking diagnostics
- [ ] **Metadata Filtering** - Filter results by metadata fields
- [ ] **Caching Layer** - Cache frequent queries for faster responses
- [ ] **Multi-language Support** - Support queries in multiple languages
- [x] **Query Rewriting Layer** - Improve retrieval robustness for short or ambiguous queries

---

## License

This project is provided as-is for educational and demonstration purposes.

---

**Happy exploring! 🎉** For questions or issues, feel free to open an issue in the repository.