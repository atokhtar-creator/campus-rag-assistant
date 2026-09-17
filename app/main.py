from pathlib import Path

from fastapi import FastAPI

from app.models import AskRequest, AskResponse
from app.retriever import KnowledgeRetriever
from app.service import AnswerService

BASE_DIR = Path(__file__).resolve().parent.parent
retriever = KnowledgeRetriever(BASE_DIR / "data" / "knowledge_base.json")
service = AnswerService(retriever)

app = FastAPI(
    title="Campus RAG Assistant",
    version="1.0.0",
    description="A lightweight source-aware university FAQ assistant.",
)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/ask", response_model=AskResponse)
def ask(payload: AskRequest) -> AskResponse:
    return AskResponse(**service.answer(payload.question))
