from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import uvicorn
import os
from models  import ChatRequest, ChatResponse, HealthRequest
from utils import logger, format_response
from runner import runner
# Create FastAPI app
app = FastAPI(
    title="EMC Helpline Assistant",
    version="1.0.0",
    description="AI Assistant for Cyberviolence Victims"
)

# CORS - Allow React to connect
origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "EMC Helpline Assistant API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health", response_model=HealthRequest)
async def health_check():
    """Health check endpoint"""
    return HealthRequest(
        status="healthy",
        version="1.0.0"
    )

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat endpoint - Send message and get AI response
    """
    try:
        logger.info(f"Received question: {request.question}")
        
        # Validate question
        if not request.question or not request.question.strip():
            raise HTTPException(
                status_code=400,
                detail="La question ne peut pas être vide."
            )
        
        # Get AI response
        response_text = runner(request.question)
        logger.info(f"Generated response: {response_text[:50]}...")
        
        return ChatResponse(
            message=response_text,
            timestamp=datetime.now()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erreur: {str(e)}"
        )

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {"error": "Not found", "status": 404}

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return {"error": "Internal server error", "status": 500}


if __name__ == "__main__":
    uvicorn.run("api:app",reload=True)