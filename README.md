# bedrock-rag-demo

🚀 **Enterprise RAG Demo with Amazon Bedrock and pgvector**

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
- [Future Improvements](#future-improvements)
- [License](#license)

---

## Overview

This project demonstrates an end-to-end Retrieval Augmented Generation (RAG) workflow that:

- 🔍 **Scrapes** the Amazon Bedrock FAQ page
- 📝 **Chunks** each FAQ into structured Q&A pairs
- 🧠 **Generates embeddings** using Amazon Bedrock's embedding models
- 💾 **Stores** embeddings in PostgreSQL with pgvector extension
- 🔎 **Performs semantic search** to retrieve relevant FAQs based on user queries

This showcases a production-style ingestion and retrieval pipeline suitable for enterprise applications.

---

## Architecture

### Ingestion Pipeline
```
FAQ Data → Chunking → Embedding Generation → Vector Storage (pgvector)
```

### Retrieval Pipeline
```
User Query → Generate Query Embedding → Vector Similarity Search → Return Top Matches
```

---

## Tech Stack

| Category | Technology |
|----------|------------|
| **Language** | Python 3.9+ |
| **AI/ML** | Amazon Bedrock |
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

---

## How It Works

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

## Future Improvements

- [ ] **Hybrid Search** - Combine keyword search with semantic search
- [ ] **Reranking Layer** - Improve result relevance with cross-encoders
- [ ] **LLM Answer Generation** - Generate answers instead of returning raw FAQs
- [ ] **FastAPI Endpoint** - Expose functionality via REST API
- [ ] **Evaluation Metrics** - Add metrics and logging for performance monitoring
- [ ] **Metadata Filtering** - Filter results by metadata fields
- [ ] **Caching Layer** - Cache frequent queries for faster responses
- [ ] **Multi-language Support** - Support queries in multiple languages

---

## License

This project is provided as-is for educational and demonstration purposes.

---

**Happy exploring! 🎉** For questions or issues, feel free to open an issue in the repository.