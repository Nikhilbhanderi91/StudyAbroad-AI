import time
from rag.retriever import RAGRetriever

def evaluate_rag_retrieval():
    print("==================================================")
    print("📊 EVALUATION: RAG RETRIEVAL ACCURACY & HIT RATE")
    print("==================================================")

    test_queries = [
        {"query": "Scholarships for Computer Science Masters in United Kingdom", "expected_type": "scholarship"},
        {"query": "Harvard University tuition and ranking in USA", "expected_type": "university_profile"},
        {"query": "Germany study guide average cost and admission requirements", "expected_type": "country_guide"},
        {"query": "Imperial College London ranking and international reputation", "expected_type": "university_profile"},
        {"query": "DAAD and engineering financial grants in Europe", "expected_type": "scholarship"}
    ]

    retriever = RAGRetriever()
    hits = 0
    latencies = []

    for item in test_queries:
        t0 = time.time()
        results = retriever.retrieve_documents(item["query"], top_k=5)
        latency = (time.time() - t0) * 1000
        latencies.append(latency)

        retrieved_types = [doc.get("document_type") for doc in results]
        is_hit = item["expected_type"] in retrieved_types
        if is_hit:
            hits += 1

        print(f"\nQuery: '{item['query']}'")
        print(f"Latency: {latency:.2f} ms | Expected Doc Type: {item['expected_type']}")
        print(f"Top-1 Retrieved: '{results[0].get('topic')}' (Score: {results[0].get('similarity_score', 0):.3f})")
        print(f"Hit Status: {'✅ SUCCESS' if is_hit else '❌ MISS'}")

    hit_rate = (hits / len(test_queries)) * 100
    avg_latency = sum(latencies) / len(latencies)
    print(f"\n==================================================")
    print(f"🎯 RESULTS: Hit Rate @ 5: {hit_rate:.1f}% | Avg Latency: {avg_latency:.2f} ms")
    print("==================================================")

if __name__ == "__main__":
    evaluate_rag_retrieval()
