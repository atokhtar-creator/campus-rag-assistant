from __future__ import annotations

import json
from pathlib import Path
from dataclasses import dataclass

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


@dataclass
class SearchResult:
    title: str
    answer: str
    score: float


class KnowledgeRetriever:
    def __init__(self, kb_path: str | Path):
        self.kb_path = Path(kb_path)
        self.items = self._load()
        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2),
            stop_words="english",
        )
        corpus = [
            f"{item['title']} {item['question']} {item['answer']}"
            for item in self.items
        ]
        self.matrix = self.vectorizer.fit_transform(corpus)

    def _load(self) -> list[dict]:
        with self.kb_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list) or not data:
            raise ValueError("Knowledge base must be a non-empty JSON list.")
        return data

    def search(self, query: str, top_k: int = 3) -> list[SearchResult]:
        query_vector = self.vectorizer.transform([query])
        scores = cosine_similarity(query_vector, self.matrix).flatten()
        ranked = scores.argsort()[::-1][:top_k]

        return [
            SearchResult(
                title=self.items[i]["title"],
                answer=self.items[i]["answer"],
                score=float(scores[i]),
            )
            for i in ranked
            if scores[i] > 0
        ]
