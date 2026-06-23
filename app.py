
import re
import joblib
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="FlowSure AI Support API")

category_model = joblib.load("flowsure_artifacts/edge_category_model.joblib")
intent_model = joblib.load("flowsure_artifacts/edge_intent_model.joblib")


def clean_text(text: str) -> str:
    text = str(text).lower()
    text = re.sub(r"http\S+", " URL ", text)
    text = re.sub(r"@\w+", " USER ", text)
    text = re.sub(r"{{.*?}}", " PLACEHOLDER ", text)
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


class TicketRequest(BaseModel):
    text: str


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/predict")
def predict_ticket(ticket: TicketRequest):
    cleaned = clean_text(ticket.text)

    category = category_model.predict([cleaned])[0]
    intent = intent_model.predict([cleaned])[0]
    confidence = float(category_model.predict_proba([cleaned]).max())

    return {
        "category": category,
        "intent": intent,
        "confidence": confidence,
    }
