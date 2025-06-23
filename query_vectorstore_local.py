from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

def search_similar_alerts(query, index_file="faiss_local.index", lines_file="wazuh_alerts_lines.txt", top_k=5):
    # Load FAISS index
    index = faiss.read_index(index_file)

    # Load stored alert lines
    with open(lines_file, "r") as f:
        alert_lines = [line.strip() for line in f if line.strip()]

    # Load sentence transformer
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Encode the query
    query_vec = model.encode([query], convert_to_numpy=True)

    # Search FAISS index
    distances, indices = index.search(query_vec, top_k)

    print(f"\n🔎 Top {top_k} results for: \"{query}\"\n")
    for i, idx in enumerate(indices[0]):
        print(f"{i+1}. {alert_lines[idx]}")
        print("-" * 80)

if __name__ == "__main__":
    question = input("🧠 Enter your threat question: ")
    search_similar_alerts(question)
