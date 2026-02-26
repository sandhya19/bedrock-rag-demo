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


def keyword_search(query_text, top_k=10):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute(
        """
        SELECT id, question, answer,
               ts_rank(search_vector, plainto_tsquery(%s)) AS rank
        FROM bedrock_faq
        ORDER BY rank DESC
        LIMIT %s;
        """,
        (query_text, top_k)
    )

    results = cur.fetchall()

    cur.close()
    conn.close()

    return results

def semantic_search(query_embedding, top_k=10):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    embedding_str = "[" + ",".join(map(str, query_embedding)) + "]"

    cur.execute(
        """
        SELECT id, question, answer,
            embedding <-> %s::vector AS distance
        FROM bedrock_faq
        ORDER BY embedding <-> %s::vector
        LIMIT %s;
        """,
        (embedding_str, embedding_str, top_k)
    )

    results = cur.fetchall()

    cur.close()
    conn.close()

    return results

def hybrid_search(query_text, top_k=3):
    query_embedding = generate_embedding(query_text)

    semantic_results = semantic_search(query_embedding, top_k=10)
    keyword_results = keyword_search(query_text, top_k=10)

    combined = {}

    # Process semantic results
    for row in semantic_results:
        id_, question, answer, distance = row
        semantic_score = 1 / (1 + distance)

        combined[id_] = {
            "question": question,
            "answer": answer,
            "semantic_score": semantic_score,
            "keyword_score": 0
        }
    
    # Normalize keyword scores
    max_keyword_rank = max(
        [row[3] for row in keyword_results],
        default=1
    )

    # Process keyword results
    for row in keyword_results:
        id_, question, answer, rank = row
        normalized_rank = rank / max_keyword_rank if max_keyword_rank > 0 else 0

        if id_ not in combined:
            combined[id_] = {
                "question": question,
                "answer": answer,
                "semantic_score": 0,
                "keyword_score": normalized_rank
            }
        else:
            combined[id_]["keyword_score"] = normalized_rank
    
    # Python exact match boost
    normalized_query = query_text.lower().strip().rstrip('?')

    # Final weighted score
    for item in combined.values():
        question_normalized = item["question"].lower().strip().rstrip('?')

        if question_normalized == normalized_query:
            exact_boost = 1
        else:
            exact_boost = 0

        item["final_score"] = (
            0.6 * item["semantic_score"] +
            0.3 * item["keyword_score"] +
            0.5 * exact_boost
        )

    # Sort by final score
    ranked = sorted(
        combined.values(),
        key=lambda x: x["final_score"],
        reverse=True
    )

    return ranked[:top_k]

if __name__ == "__main__":
    user_query = input("Ask a question about Amazon Bedrock: ")

    results = hybrid_search(user_query)

    print("\nHybrid Search Results:\n")

    for i, item in enumerate(results, 1):
        print(f"{i}. {item['question']} (score={item['final_score']:.4f})")
        print(item["answer"])
        print("-" * 50)