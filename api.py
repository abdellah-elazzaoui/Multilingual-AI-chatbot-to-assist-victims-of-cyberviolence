# api.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.app.runner import runner

app = FastAPI(title="EMC Helpline Assistant")

# CORS middleware - Allows React to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React's default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    question: str

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/chat")
def chat_model(request: ChatRequest):
    if not request.question:
        raise HTTPException(
            status_code=400,
            detail="La question ne peut pas être vide."
        )
    try:
        response = runner(question=request.question)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Une erreur est survenue lors du traitement de votre question: {e}"
        )    
    return {"message": response}  # Returns {"message": "response_text"}