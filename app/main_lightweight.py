"""
FastAPI application for SmartSupport AI (Lightweight version for free tier)
Uses rule-based classification instead of ML models
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
from contextlib import asynccontextmanager
import time
import os

from app.inference_lightweight import classifier


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    print("\n" + "="*60)
    print("SmartSupport AI - Lightweight Mode")
    print("="*60)
    print("✓ Server starting on port", os.getenv("PORT", "8000"))
    print("✓ Using rule-based classifier (no ML model)")
    
    yield
    
    print("\nSmartSupport AI stopped")


app = FastAPI(
    title="SmartSupport AI (Lightweight)",
    description="Rule-based ticket classification system optimized for free tier deployment",
    version="2.0.0-lite",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for free tier
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TicketInput(BaseModel):
    """Input model for ticket prediction"""
    text: str = Field(
        ..., 
        min_length=10,
        max_length=1000,
        description="Support ticket text (10-1000 characters)"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "text": "I was charged twice for my subscription this month"
            }
        }


class PredictionResponse(BaseModel):
    """Response model for predictions"""
    category: str = Field(..., description="Predicted category")
    category_confidence: float = Field(..., description="Category confidence score (0-1)")
    priority: str = Field(..., description="Predicted priority level")
    priority_confidence: float = Field(..., description="Priority confidence score (0-1)")
    inference_time_ms: float = Field(..., description="Inference time in milliseconds")
    model: str = Field(..., description="Model used for prediction")
    
    class Config:
        json_schema_extra = {
            "example": {
                "category": "Billing",
                "category_confidence": 0.9234,
                "priority": "High",
                "priority_confidence": 0.8756,
                "inference_time_ms": 2.45,
                "model": "rule-based-v1"
            }
        }


@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "service": "SmartSupport AI (Lightweight)",
        "version": "2.0.0-lite",
        "description": "Rule-based ticket classification system",
        "model": "rule-based-v1",
        "categories": ["General", "Account", "Billing", "Technical"],
        "priorities": ["Low", "Medium", "High"],
        "endpoints": {
            "predict": "POST /predict",
            "health": "GET /health",
            "docs": "GET /docs"
        },
        "note": "This is a lightweight version optimized for free tier deployment"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": True,
        "model": "rule-based-v1",
        "categories": ["General", "Account", "Billing", "Technical"],
        "priorities": ["Low", "Medium", "High"]
    }


@app.post("/predict", response_model=PredictionResponse)
async def predict_ticket(ticket: TicketInput):
    """
    Classify and prioritize a support ticket using rule-based system.
    
    This endpoint uses keyword matching to:
    - Classify the ticket into categories (Billing, Technical, Account, General)
    - Assign priority levels (High, Medium, Low)
    - Provide confidence scores for both predictions
    """
    try:
        start_time = time.time()
        
        # Get prediction from rule-based classifier
        result = classifier.predict(ticket.text)
        
        total_time = (time.time() - start_time) * 1000
        
        return PredictionResponse(
            category=result['category'],
            category_confidence=result['category_confidence'],
            priority=result['priority'],
            priority_confidence=result['priority_confidence'],
            inference_time_ms=round(total_time, 2),
            model="rule-based-v1"
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
