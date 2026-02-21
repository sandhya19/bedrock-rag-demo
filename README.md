# bedrock-rag-demo
Enterprise RAG Demo with Amazon Bedrock and pgvector
Overview

This project demonstrates an end to end Retrieval Augmented Generation workflow using:

• Amazon Bedrock for embeddings
• PostgreSQL with pgvector for vector storage
• Semantic similarity search for retrieval

The demo scrapes the Amazon Bedrock FAQ page, converts each FAQ into structured chunks, generates embeddings, stores them in a vector database, and performs semantic search over the content.

This showcases a production style ingestion and retrieval pipeline.

# Architecture

# Ingestion Layer
Scrape FAQ → Chunk Q and A → Generate Embeddings → Store in pgvector

# Retrieval Layer
User Query → Generate Query Embedding → Vector Similarity Search → Return Top Matches

# Tech Stack
• Python
• Amazon Bedrock
• PostgreSQL with pgvector
• Docker
• BeautifulSoup
• psycopg2

# Project Structure
bedrock-rag-demo/
scraper/
  scrape_bedrock_faq.py
  bedrock_faq.json
ingestion/
  chunk_and_prepare.py
  embed_all_chunks.py
  test_embedding.py
  bedrock_chunks.json
  bedrock_chunks_with_embeddings.json
storage/
  load_into_pgvector.py
retrieval/
  query_service.py
requirements.txt
README.md

# Prerequisites
• Python 3.9+
• AWS CLI configured
• Bedrock model access enabled
• Docker installed

**Step 1:** Install Dependencies

pip install -r requirements.txt
requirements.txt should contain:
boto3
requests
beautifulsoup4
psycopg2-binary

**Step 2:** Scrape Amazon Bedrock FAQ

Run:

python scraper/scrape_bedrock_faq.py

This creates:

scraper/bedrock_faq.json

**Step 3:** Prepare Q and A Chunks

Run:

python ingestion/chunk_and_prepare.py

This creates:

ingestion/bedrock_chunks.json

Each chunk contains:

• id
• question
• answer
• combined text

**Step 4:** Generate Embeddings with Bedrock

Test embedding access first:

python ingestion/test_embedding.py

Then generate embeddings for all chunks:

python ingestion/embed_all_chunks.py

This creates:

ingestion/bedrock_chunks_with_embeddings.json

**Step 5:** Start PostgreSQL with pgvector

Run:

docker run -d
--name pgvector-demo
-e POSTGRES_PASSWORD=postgres
-p 5432:5432
ankane/pgvector

Verify container is running:

docker ps

**Step 6:** Create Database Table

Connect to container:

docker exec -it pgvector-demo psql -U postgres

Inside PostgreSQL:

CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE bedrock_faq (
id TEXT PRIMARY KEY,
question TEXT,
answer TEXT,
embedding VECTOR(1536)
);

Exit with:

\q

**Step 7:** Load Data into Database

Run:

python storage/load_into_pgvector.py

You should see:

Data inserted successfully.

**Step 8:** Run Semantic Search

Run:

python retrieval/query_service.py

Enter a question such as:

What is Amazon Bedrock?
How much does Amazon Bedrock cost?
Which models are supported?

The system will:

• Generate query embedding
• Perform vector similarity search
• Return top matching FAQ entries

# How Similarity Search Works

The query embedding is compared against stored embeddings using pgvector distance operator:

embedding <-> query_vector

The lowest distance values are most similar.

# Future Improvements

• Add hybrid keyword plus semantic search
• Add reranking layer
• Add LLM answer generation
• Add FastAPI API endpoint
• Add evaluation metrics and logging
• Add metadata filtering

What This Demonstrates

• End to end RAG ingestion pipeline
