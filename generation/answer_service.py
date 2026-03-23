import boto3
import json

bedrock = boto3.client("bedrock-runtime")

def call_bedrock_llm(prompt):
    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 500,
        "temperature": 0.2,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }
    response = bedrock.invoke_model(
        modelId="anthropic.claude-3-sonnet-20240229-v1:0",
        body=json.dumps(body)
    )

    result = json.loads(response["body"].read())
    return result["content"][0]["text"]


def build_prompt(query, context):
    return f"""
You are a knowledgeable assistant.

Using ONLY the information provided in the context below, write a clear, concise, and natural answer to the user's question.

Do NOT mention "Source" numbers inside the answer.
Do NOT say "According to the context".
Do NOT copy the FAQ wording verbatim.

Synthesize the information into a helpful explanation.


If the answer is not present in the provided context, say:
"I do not have enough information in the knowledge base to answer this question."

Context:
{context}

User Question:
{query}

Answer:
"""


def build_context(chunks):
    context_parts = []
    for i, chunk in enumerate(chunks):
        context_parts.append(
            f"Source {i+1}:\nQuestion: {chunk['question']}\nAnswer: {chunk['answer']}\n"
        )
    return "\n".join(context_parts)


def generate_answer(query, retrieved_chunks):
    context = build_context(retrieved_chunks)
    prompt = build_prompt(query, context)
    response = call_bedrock_llm(prompt)
    return response