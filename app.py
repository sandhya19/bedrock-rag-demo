from retrieval.query_service import hybrid_search
from generation.answer_service import generate_answer

def main():
    query = input("Ask a question: ")

    retrieved = hybrid_search(query, top_k=3)

    print("\nTop Retrieved Chunks:")
    for r in retrieved:
        print("-", r["question"])

    answer = generate_answer(query, retrieved)

    print("\nGenerated Answer:\n")
    print(answer)

if __name__ == "__main__":
    main()