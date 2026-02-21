import boto3
import json
import os
import time

REGION = "eu-central-1"  # change if your Bedrock access is in another region
MODEL_ID = "amazon.titan-embed-text-v1"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(BASE_DIR, "bedrock_chunks.json")
OUTPUT_FILE = os.path.join(BASE_DIR, "bedrock_chunks_with_embeddings.json")

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


def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    for i, chunk in enumerate(chunks):
        print(f"Embedding chunk {i+1}/{len(chunks)}")

        embedding = generate_embedding(chunk["text"])
        chunk["embedding"] = embedding

        # small delay to avoid aggressive calls
        time.sleep(0.1)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(chunks, f)

    print("All chunks embedded successfully.")


if __name__ == "__main__":
    main()