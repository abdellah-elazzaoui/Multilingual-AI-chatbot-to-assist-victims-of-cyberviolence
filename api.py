from fastapi import FastAPI
from runner import runner
app = FastAPI()
@app.get("/chat")
def chat_model(question:str):
    response = runner(question=question)
    return {"message":response}
