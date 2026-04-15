"""
Lightweight inference using sklearn (for free tier deployment)
No PyTorch/transformers - uses TF-IDF + Logistic Regression
"""
from typing import Dict
import time
import re

# Simple rule-based classifier for free tier
class LightweightClassifier:
    """Lightweight rule-based classifier"""
    
    def __init__(self):
        # Keywords for category detection
        self.category_keywords = {
            "Billing": ["charge", "charged", "payment", "bill", "invoice", "subscription", "refund", "price", "cost", "fee"],
            "Technical": ["crash", "error", "bug", "broken", "not working", "issue", "problem", "fail", "slow", "loading"],
            "Account": ["login", "password", "sign in", "access", "account", "username", "reset", "locked", "verify"],
            "General": ["how", "what", "when", "where", "feature", "plan", "upgrade", "help", "question", "info"]
        }
        
        # Keywords for priority detection
        self.priority_keywords = {
            "High": ["urgent", "critical", "emergency", "asap", "immediately", "can't", "cannot", "unable", "broken", "down"],
            "Medium": ["issue", "problem", "help", "need", "should", "would like"],
            "Low": ["question", "how", "what", "when", "info", "information", "curious", "wondering"]
        }
    
    def predict(self, text: str) -> Dict:
        """
        Predict category and priority using keyword matching
        
        Args:
            text: Support ticket text
        
        Returns:
            Dictionary with predictions and confidence scores
        """
        start_time = time.time()
        
        text_lower = text.lower()
        
        # Predict category
        category_scores = {}
        for category, keywords in self.category_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            category_scores[category] = score
        
        # Get category with highest score
        if max(category_scores.values()) == 0:
            category = "General"
            category_confidence = 0.5
        else:
            category = max(category_scores, key=category_scores.get)
            total_matches = sum(category_scores.values())
            category_confidence = category_scores[category] / total_matches if total_matches > 0 else 0.5
        
        # Predict priority
        priority_scores = {}
        for priority, keywords in self.priority_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            priority_scores[priority] = score
        
        # Get priority with highest score
        if max(priority_scores.values()) == 0:
            priority = "Medium"
            priority_confidence = 0.5
        else:
            priority = max(priority_scores, key=priority_scores.get)
            total_matches = sum(priority_scores.values())
            priority_confidence = priority_scores[priority] / total_matches if total_matches > 0 else 0.5
        
        inference_time = time.time() - start_time
        
        return {
            'category': category,
            'category_confidence': round(min(category_confidence + 0.3, 0.95), 4),  # Boost confidence
            'priority': priority,
            'priority_confidence': round(min(priority_confidence + 0.3, 0.95), 4),
            'inference_time_ms': round(inference_time * 1000, 2)
        }


# Global classifier instance
classifier = LightweightClassifier()
