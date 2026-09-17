from app.retriever import KnowledgeRetriever


class AnswerService:
    def __init__(self, retriever: KnowledgeRetriever, min_score: float = 0.05):
        self.retriever = retriever
        self.min_score = min_score

    def answer(self, question: str) -> dict:
        results = self.retriever.search(question, top_k=3)

        if not results or results[0].score < self.min_score:
            return {
                "answer": (
                    "I could not find a reliable answer in the approved knowledge base. "
                    "Please contact the relevant support team."
                ),
                "sources": [],
            }

        best = results[0]
        return {
            "answer": best.answer,
            "sources": [
                {"title": item.title, "score": round(item.score, 4)}
                for item in results
            ],
        }
