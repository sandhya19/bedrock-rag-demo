import boto3
import json
import psycopg2

REGION = "eu-central-1"  # change if your Bedrock access is in another region
MODEL_ID = "amazon.titan-embed-text-v1"

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "postgres",
    "user": "postgres",
    "password": "postgres"
}

client = boto3.client("bedrock-runtime", region_name=REGION)


def generate_embedding(text):
    body = {"inputText": text}

    response = client.invoke_model(
        modelId=MODEL_ID,
        body=json.dumps(body),
        contentType="application/json",
        accept="application/json"
    )

    response_body = json.loads(response["body"].read())
    return response_body["embedding"]


def search_similar(query_embedding, top_k=3):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    embedding_str = "[" + ",".join(map(str, query_embedding)) + "]"

    cur.execute(
        """
        SELECT question, answer
        FROM bedrock_faq
        ORDER BY embedding <-> %s::vector
        LIMIT %s;
        """,
        (embedding_str, top_k)
    )

    results = cur.fetchall()

    cur.close()
    conn.close()

    return results

if __name__ == "__main__":
    user_query = input("Ask a question about Amazon Bedrock: ")

    query_embedding = generate_embedding(user_query)

    results = search_similar(query_embedding)

    print("\nTop Results:\n")

    for i, (question, answer) in enumerate(results, 1):
        print(f"{i}. {question}")
        print(answer)
        print("-" * 50)