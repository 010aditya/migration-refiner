import json
import os
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from typing import List

class MappingVerifierAgent:
    def __init__(self, threshold=0.3):
        self.threshold = threshold
        self.embedding = OpenAIEmbeddings()
        self.splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

    def embed_file(self, filepath: str) -> List[Document]:
        try:
            with open(filepath, 'r', errors='ignore') as f:
                content = f.read()
                return self.splitter.create_documents([content])
        except Exception:
            return []

    def cosine_similarity(self, d1: str, d2: str) -> float:
        docs = self.embedding.embed_documents([d1, d2])
        v1, v2 = docs[0], docs[1]
        dot = sum(x * y for x, y in zip(v1, v2))
        norm1 = sum(x ** 2 for x in v1) ** 0.5
        norm2 = sum(x ** 2 for x in v2) ** 0.5
        return dot / (norm1 * norm2 + 1e-9)

    def verify(self, mapping_file: str):
        with open(mapping_file) as f:
            mappings = json.load(f)

        valid, invalid = [], []
        for m in mappings:
            src = m['sourcePath']
            tgt = m['targetPath']
            if not (os.path.exists(src) and os.path.exists(tgt)):
                invalid.append({**m, "reason": "Missing file(s)"})
                continue

            src_doc = self.embed_file(src)
            tgt_doc = self.embed_file(tgt)
            if not src_doc or not tgt_doc:
                invalid.append({**m, "reason": "Unreadable content"})
                continue

            sim = self.cosine_similarity(src_doc[0].page_content, tgt_doc[0].page_content)
            if sim >= self.threshold:
                valid.append({**m, "similarity": round(sim, 3)})
            else:
                invalid.append({**m, "similarity": round(sim, 3), "reason": "Low similarity"})

        with open("mapping.verified.json", "w") as f:
            json.dump(valid, f, indent=2)
        with open("mapping_verification.log", "w") as f:
            json.dump(invalid, f, indent=2)
