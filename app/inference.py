"""
Inference utilities for ticket classification
"""
from typing import Dict
import time

from ml.config import Config
from app.model_loader import model_loader


class TicketClassifier:
    """Inference class for ticket classification"""
    
    def __init__(self):
        self.model = None
        self.tokenizer = None
    
    def load(self):
        """Load model and tokenizer"""
        self.model, self.tokenizer = model_loader.load_model()
    
    def predict(self, text: str) -> Dict:
        """
        Predict category and priority for a ticket
        
        Args:
            text: Support ticket text
        
        Returns:
            Dictionary with predictions and confidence scores
        """
        # Import torch only when needed
        import torch
        
        if self.model is None or self.tokenizer is None:
            self.load()
        
        start_time = time.time()
        
        # Tokenize
        encoding = self.tokenizer(
            text,
            add_special_tokens=True,
            max_length=Config.MAX_LENGTH,
            padding='max_length',
            truncation=True,
            return_attention_mask=True,
            return_tensors='pt'
        )
        
        # Move to device
        input_ids = encoding['input_ids'].to(Config.DEVICE)
        attention_mask = encoding['attention_mask'].to(Config.DEVICE)
        
        # Predict
        self.model.eval()
        with torch.no_grad():
            category_pred, category_conf, priority_pred, priority_conf = self.model.predict(
                input_ids, attention_mask
            )
        
        # Convert to Python types
        category_id = category_pred.item()
        category_confidence = category_conf.item()
        priority_id = priority_pred.item()
        priority_confidence = priority_conf.item()
        
        # Get names
        category_name = Config.get_category_name(category_id)
        priority_name = Config.get_priority_name(priority_id)
        
        inference_time = time.time() - start_time
        
        return {
            'category': category_name,
            'category_confidence': round(category_confidence, 4),
            'priority': priority_name,
            'priority_confidence': round(priority_confidence, 4),
            'inference_time_ms': round(inference_time * 1000, 2)
        }
    
    def predict_batch(self, texts: list) -> list:
        """
        Predict for multiple tickets
        
        Args:
            texts: List of support ticket texts
        
        Returns:
            List of prediction dictionaries
        """
        if self.model is None or self.tokenizer is None:
            self.load()
        
        results = []
        for text in texts:
            result = self.predict(text)
            results.append(result)
        
        return results


# Global classifier instance
classifier = TicketClassifier()


if __name__ == "__main__":
    # Test inference
    test_tickets = [
        "I was charged twice for my subscription",
        "Cannot login to my account",
        "How do I change my password",
        "What features are in the pro plan"
    ]
    
    print("Testing inference...")
    for ticket in test_tickets:
        print(f"\nTicket: {ticket}")
        result = classifier.predict(ticket)
        print(f"Category: {result['category']} (confidence: {result['category_confidence']})")
        print(f"Priority: {result['priority']} (confidence: {result['priority_confidence']})")
        print(f"Inference time: {result['inference_time_ms']}ms")
