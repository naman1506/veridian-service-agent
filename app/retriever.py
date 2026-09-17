from __future__ import annotations
import re
from rank_bm25 import BM25Okapi
from .ingest import knowledge_base

class Retriever:
    def __init__(self):
        self.docs = knowledge_base()
        self.tokens = [self._tokens(d["title"] + " " + d["text"] + " " + " ".join(d["aliases"])) for d in self.docs]
        self.bm25 = BM25Okapi(self.tokens)
    def _tokens(self, text): return re.findall(r"[a-z0-9]+", text.lower())
    def search(self, query: str, k: int = 4):
        q = self._tokens(query); scores = self.bm25.get_scores(q)
        for i, doc in enumerate(self.docs):
            aliases = " ".join(doc["aliases"]).lower()
            scores[i] += sum(2 for token in q if token in aliases)
        ranked = sorted(range(len(self.docs)), key=lambda i: scores[i], reverse=True)[:k]
        return [{**self.docs[i], "score":round(float(scores[i]), 3)} for i in ranked]
