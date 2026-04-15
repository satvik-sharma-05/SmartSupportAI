"""
FastAPI application for SmartSupport AI
Production-grade transformer-based ticket classification API
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
from contextlib import asynccontextmanager
import time
import os

from app.database import db
from app.inference import classifier
from ml.config import Config


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    print("\n" + "="*60)
    print("SmartSupport AI - Starting...")
    print("="*60)
    print("✓ Server starting on port", os.getenv("PORT", "8000"))
    
    # Start server first, then load model in background
    yield
    
    # Shutdown
    try:
        db.close()
    except:
        pass
    print("\nSmartSupport AI stopped")


app = FastAPI(
    title="SmartSupport AI",
    description="Production-grade transformer-based ticket classification and prioritization system",
    version="2.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ],
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
    ticket_id: Optional[str] = Field(None, description="Ticket ID (if database enabled)")
    category: str = Field(..., description="Predicted category")
    category_confidence: float = Field(..., description="Category confidence score (0-1)")
    priority: str = Field(..., description="Predicted priority level")
    priority_confidence: float = Field(..., description="Priority confidence score (0-1)")
    inference_time_ms: float = Field(..., description="Inference time in milliseconds")
    model: str = Field(..., description="Model used for prediction")
    
    class Config:
        json_schema_extra = {
            "example": {
                "ticket_id": "507f1f77bcf86cd799439011",
                "category": "Billing",
                "category_confidence": 0.9234,
                "priority": "High",
                "priority_confidence": 0.8756,
                "inference_time_ms": 145.23,
                "model": "microsoft/deberta-v3-base"
            }
        }


@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "service": "SmartSupport AI",
        "version": "2.0.0",
        "description": "Transformer-based ticket classification system",
        "model": Config.MODEL_NAME,
        "device": str(Config.DEVICE),
        "categories": Config.CATEGORIES,
        "priorities": Config.PRIORITIES,
        "endpoints": {
            "predict": "POST /predict",
            "health": "GET /health",
            "tickets": "GET /tickets",
            "predictions": "GET /predictions",
            "statistics": "GET /statistics",
            "docs": "GET /docs"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        import os
        
        # Check if model is loaded
        model_loaded = classifier.model is not None
        
        # Check if model file exists (might be downloading)
        model_exists = os.path.exists("models/smartsupport_model/model.pt")
        
        # Check database connection
        db_connected = db.client is not None
        
        status = "healthy"
        if not model_loaded and not model_exists:
            status = "starting"  # Model still downloading
        elif not model_loaded and model_exists:
            status = "ready"  # Model downloaded but not loaded yet
        
        return {
            "status": status,
            "model_loaded": model_loaded,
            "model_exists": model_exists,
            "database_connected": db_connected,
            "model": Config.MODEL_NAME,
            "device": str(Config.DEVICE),
            "categories": Config.CATEGORIES,
            "priorities": Config.PRIORITIES
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Health check failed: {str(e)}")


@app.post("/predict", response_model=PredictionResponse)
async def predict_ticket(ticket: TicketInput):
    """
    Classify and prioritize a support ticket using transformer model.
    
    This endpoint uses a fine-tuned DeBERTa/RoBERTa model to:
    - Classify the ticket into categories (Billing, Technical, Account, General)
    - Assign priority levels (High, Medium, Low)
    - Provide confidence scores for both predictions
    
    The model uses multi-task learning to jointly predict category and priority.
    """
    try:
        import os
        start_time = time.time()
        
        # Check if model file exists
        if not os.path.exists("models/smartsupport_model/model.pt"):
            raise HTTPException(
                status_code=503,
                detail="Model is still downloading. Please try again in a few moments."
            )
        
        # Load model on first request (lazy loading)
        if classifier.model is None:
            print("Loading model on first request...")
            classifier.load()
            print("✓ Model loaded successfully")
        
        # Get prediction from transformer model
        result = classifier.predict(ticket.text)
        
        # Store in database if available
        ticket_id = None
        if db.tickets:
            ticket_id = db.insert_ticket(ticket.text)
            if ticket_id:
                db.insert_prediction(
                    ticket_id,
                    result['category'],
                    result['category_confidence'],
                    result['priority'],
                    result['priority_confidence'],
                    result['inference_time_ms']
                )
        
        total_time = (time.time() - start_time) * 1000
        
        return PredictionResponse(
            ticket_id=ticket_id,
            category=result['category'],
            category_confidence=result['category_confidence'],
            priority=result['priority'],
            priority_confidence=result['priority_confidence'],
            inference_time_ms=round(total_time, 2),
            model=Config.MODEL_NAME
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )


@app.get("/tickets")
async def get_tickets(limit: int = 100):
    """
    Retrieve stored tickets from database.
    
    Args:
        limit: Maximum number of tickets to return (default: 100)
    """
    try:
        tickets = db.get_tickets(limit)
        return {
            "count": len(tickets),
            "tickets": tickets
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve tickets: {str(e)}"
        )


@app.get("/predictions")
async def get_predictions(limit: int = 100):
    """
    Retrieve prediction history from database.
    
    Args:
        limit: Maximum number of predictions to return (default: 100)
    """
    try:
        predictions = db.get_predictions(limit)
        return {
            "count": len(predictions),
            "predictions": predictions
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve predictions: {str(e)}"
        )


@app.get("/statistics")
async def get_statistics():
    """
    Get database statistics and analytics.
    
    Returns:
        - Total tickets and predictions
        - Category distribution
        - Priority distribution
        - Average inference time
    """
    try:
        stats = db.get_statistics()
        return stats
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve statistics: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
