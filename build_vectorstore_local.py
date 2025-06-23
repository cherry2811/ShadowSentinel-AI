from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

def build_vectorstore_local(input_file="wazuh_alerts.txt", index_file="faiss_local.index"):
    # Load alerts
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    # Load local sentence transformer model
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Embed all lines
    embeddings = model.encode(lines, convert_to_numpy=True)

    # Build FAISS index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    # Save index and lines
    faiss.write_index(index, index_file)

    with open("wazuh_alerts_lines.txt", "w") as f:
        for line in lines:
            f.write(line + "\n")

    print(f"✅ Built local FAISS index and saved as {index_file}")

if __name__ == "__main__":
    build_vectorstore_local()
