import boto3
import json

REGION = "eu-central-1"  # change if your Bedrock access is in another region

client = boto3.client("bedrock-runtime", region_name=REGION)

def generate_embedding(text):
    body = {
        "inputText": text
    }

    response = client.invoke_model(
        modelId="amazon.titan-embed-text-v1",
        body=json.dumps(body),
        contentType="application/json",
        accept="application/json"
    )

    response_body = json.loads(response["body"].read())
    return response_body["embedding"]


if __name__ == "__main__":
    test_text = "What is Amazon Bedrock?"
    embedding = generate_embedding(test_text)

    print("Embedding length:", len(embedding))
    print("First 5 values:", embedding[:5])