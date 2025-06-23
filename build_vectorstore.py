from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

def build_vectorstore(file_path="wazuh_alerts.txt"):
    # Load raw text file
    with open(file_path, "r") as f:
        raw_text = f.read()

    # Split text into chunks (1000 chars with 100 overlap)
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    texts = splitter.split_text(raw_text)

    # Create OpenAI embeddings
    embeddings = OpenAIEmbeddings()

    # Create FAISS vector store from texts and embeddings
    vectorstore = FAISS.from_texts(texts, embeddings)

    # Save vector store to disk
    vectorstore.save_local("faiss_index")

    print("✅ Vector store built and saved as 'faiss_index'")

if __name__ == "__main__":
    build_vectorstore()
