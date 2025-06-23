from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class ThreatMemory:
    def __init__(self):
        self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        self.alerts = []
        self.ips = []
        self.index = faiss.IndexFlatL2(384)  # 384-dim embeddings from model

    def add_alert(self, summary, ip):
        emb = self.model.encode([summary])
        self.index.add(np.array(emb).astype('float32'))
        self.alerts.append(summary)
        self.ips.append(ip)

    def find_similar(self, summary, threshold=0.4):
        if len(self.alerts) == 0:
            return None
        emb = self.model.encode([summary])
        D, I = self.index.search(np.array(emb).astype('float32'), 1)
        if D[0][0] < threshold:
            idx = I[0][0]
            return {'summary': self.alerts[idx], 'ip': self.ips[idx]}
        return None
