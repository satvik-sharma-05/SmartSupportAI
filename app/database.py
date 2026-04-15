"""
MongoDB database integration for SmartSupport AI
"""
from pymongo import MongoClient
from datetime import datetime
from typing import Optional, List, Dict
import os
from dotenv import load_dotenv

load_dotenv()


class Database:
    """MongoDB database handler"""
    
    def __init__(self):
        self.client = None
        self.db = None
        self.tickets = None
        self.predictions = None
    
    def connect(self):
        """Connect to MongoDB"""
        try:
            mongo_uri = os.getenv('MONGO_URI')
            db_name = os.getenv('MONGO_DB_NAME', 'smartsupport_ai')
            
            if not mongo_uri:
                print("⚠️  MONGO_URI not set. Database features disabled.")
                return False
            
            self.client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
            self.db = self.client[db_name]
            
            # Collections
            self.tickets = self.db['tickets']
            self.predictions = self.db['predictions']
            
            # Test connection
            self.client.server_info()
            print(f"✓ Connected to MongoDB: {db_name}")
            return True
        except Exception as e:
            print(f"⚠️  Database connection failed: {e}")
            print("   Predictions will work but won't be stored.")
            return False
    
    def insert_ticket(self, text: str) -> Optional[str]:
        """Insert a new ticket"""
        if not self.tickets:
            return None
        
        try:
            ticket = {
                "text": text,
                "created_at": datetime.utcnow()
            }
            result = self.tickets.insert_one(ticket)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error inserting ticket: {e}")
            return None
    
    def insert_prediction(self, ticket_id: str, category: str, 
                         category_confidence: float, priority: str,
                         priority_confidence: float, inference_time_ms: float) -> Optional[str]:
        """Insert prediction result"""
        if not self.predictions:
            return None
        
        try:
            prediction = {
                "ticket_id": ticket_id,
                "category": category,
                "category_confidence": category_confidence,
                "priority": priority,
                "priority_confidence": priority_confidence,
                "inference_time_ms": inference_time_ms,
                "timestamp": datetime.utcnow()
            }
            result = self.predictions.insert_one(prediction)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error inserting prediction: {e}")
            return None
    
    def get_tickets(self, limit: int = 100) -> List[Dict]:
        """Retrieve tickets"""
        if not self.tickets:
            return []
        
        try:
            tickets = list(self.tickets.find().sort("created_at", -1).limit(limit))
            for ticket in tickets:
                ticket['_id'] = str(ticket['_id'])
            return tickets
        except Exception as e:
            print(f"Error retrieving tickets: {e}")
            return []
    
    def get_predictions(self, limit: int = 100) -> List[Dict]:
        """Retrieve predictions"""
        if not self.predictions:
            return []
        
        try:
            predictions = list(self.predictions.find().sort("timestamp", -1).limit(limit))
            for pred in predictions:
                pred['_id'] = str(pred['_id'])
            return predictions
        except Exception as e:
            print(f"Error retrieving predictions: {e}")
            return []
    
    def get_statistics(self) -> Dict:
        """Get database statistics"""
        if not self.tickets or not self.predictions:
            return {}
        
        try:
            stats = {
                "total_tickets": self.tickets.count_documents({}),
                "total_predictions": self.predictions.count_documents({}),
                "category_distribution": list(self.predictions.aggregate([
                    {"$group": {"_id": "$category", "count": {"$sum": 1}}}
                ])),
                "priority_distribution": list(self.predictions.aggregate([
                    {"$group": {"_id": "$priority", "count": {"$sum": 1}}}
                ])),
                "avg_inference_time_ms": list(self.predictions.aggregate([
                    {"$group": {"_id": None, "avg_time": {"$avg": "$inference_time_ms"}}}
                ]))
            }
            return stats
        except Exception as e:
            print(f"Error getting statistics: {e}")
            return {}
    
    def close(self):
        """Close database connection"""
        if self.client:
            self.client.close()
            print("✓ Database connection closed")


# Global database instance
db = Database()
