import json
import time
from retrieval.query_service import hybrid_search

def evaluate():
    with open("evaluation/test_queries.json") as f:
        test_data = json.load(f)

    total = len(test_data)
    correct_at_1 = 0
    correct_at_3 = 0

    total_latency = 0
    print(total, "test queries found. Starting evaluation...")
    for item in test_data:
        query = item["query"]
        expected_id = item["expected_id"]

        start = time.time()
        results = hybrid_search(query, top_k=3)
        end = time.time()

        latency = end - start
        total_latency += latency

        returned_ids = [r["id"] for r in results]

        if expected_id != returned_ids[0]:
            print("Misranked query:", query)
            print("Top result:", results[0]["question"])
            print("Expected:", expected_id)
            print("-----")

        

        if expected_id == returned_ids[0]:
            correct_at_1 += 1

        if expected_id in returned_ids:
            correct_at_3 += 1

    
    print("Precision@1:", correct_at_1 / total)
    print("Precision@3:", correct_at_3 / total)
    print("Avg Latency:", total_latency / total)

if __name__ == "__main__":
    evaluate()