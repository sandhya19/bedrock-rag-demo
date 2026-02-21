import json
import uuid

INPUT_FILE = "../scraper/bedrock_faq.json"
OUTPUT_FILE = "bedrock_chunks.json"


def load_faq(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


def create_chunks(faq_data):
    chunks = []

    for item in faq_data:
        chunk_id = str(uuid.uuid4())

        question = item["question"].strip()
        answer = item["answer"].strip()

        chunk_text = f"Question: {question}\nAnswer: {answer}"

        chunks.append({
            "id": chunk_id,
            "question": question,
            "answer": answer,
            "text": chunk_text,
            "source": "aws_bedrock_faq"
        })

    return chunks


def save_chunks(chunks, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)


def main():
    faq_data = load_faq(INPUT_FILE)
    chunks = create_chunks(faq_data)
    save_chunks(chunks, OUTPUT_FILE)
    print(f"Prepared {len(chunks)} chunks for embedding.")


if __name__ == "__main__":
    main()