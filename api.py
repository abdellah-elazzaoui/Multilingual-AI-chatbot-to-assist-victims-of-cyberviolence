from fastapi import FastAPI,HTTPException
from runner import runner
from pydantic import BaseModel,Field

app = FastAPI(title="EMC Helpline Assistant")


@app.get("/chat")
def chat_model(question:str):
    if not question:
        return HTTPException(
            status_code=400,
            detail="La question ne peut pas être vide."
        )
    try:
        response = runner(question=question)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail= f"Une erreur est survenue lors du traitement de votre question: {e}"
        )    
    return {"message":response}