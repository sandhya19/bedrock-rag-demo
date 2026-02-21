import json
import psycopg2

DB_CONFIG = {
    "host": "localhost",
    "database": "postgres",
    "user": "postgres",
    "password": "postgres"
}

INPUT_FILE = "ingestion/bedrock_chunks_with_embeddings.json"

def main():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    for chunk in chunks:
        cur.execute(
            """
            INSERT INTO bedrock_faq (id, question, answer, embedding)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
            """,
            (
                chunk["id"],
                chunk["question"],
                chunk["answer"],
                chunk["embedding"]
            )
        )

    conn.commit()
    cur.close()
    conn.close()

    print("Data inserted successfully.")

if __name__ == "__main__":
    main()