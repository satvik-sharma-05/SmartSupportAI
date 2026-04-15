"""
Multi-task transformer model for ticket classification
"""
import torch
import torch.nn as nn
from transformers import AutoModel, AutoConfig
from ml.config import Config


class MultiTaskTicketClassifier(nn.Module):
    """
    Multi-task learning model that predicts both category and priority
    using a shared transformer encoder
    """
    
    def __init__(self, model_name: str = Config.MODEL_NAME, num_categories: int = None, num_priorities: int = None):
        super(MultiTaskTicketClassifier, self).__init__()
        
        # Use provided values or defaults from config
        if num_categories is None:
            num_categories = Config.NUM_CATEGORIES
        if num_priorities is None:
            num_priorities = Config.NUM_PRIORITIES
        
        # Load pretrained transformer
        self.config = AutoConfig.from_pretrained(model_name)
        self.transformer = AutoModel.from_pretrained(model_name)
        
        # Get hidden size from transformer config
        hidden_size = self.config.hidden_size
        
        # Dropout for regularization
        dropout_rate = 0.3
        
        # Category classification head (matches Colab architecture)
        self.category_classifier = nn.Sequential(
            nn.Dropout(dropout_rate),
            nn.Linear(hidden_size, hidden_size // 2),
            nn.ReLU(),
            nn.Dropout(dropout_rate),
            nn.Linear(hidden_size // 2, num_categories)
        )
        
        # Priority classification head (matches Colab architecture)
        self.priority_classifier = nn.Sequential(
            nn.Dropout(dropout_rate),
            nn.Linear(hidden_size, hidden_size // 2),
            nn.ReLU(),
            nn.Dropout(dropout_rate),
            nn.Linear(hidden_size // 2, num_priorities)
        )
    
    def forward(self, input_ids, attention_mask):
        """
        Forward pass
        
        Args:
            input_ids: Token IDs [batch_size, seq_length]
            attention_mask: Attention mask [batch_size, seq_length]
        
        Returns:
            category_logits: Category predictions [batch_size, num_categories]
            priority_logits: Priority predictions [batch_size, num_priorities]
        """
        # Get transformer outputs
        outputs = self.transformer(
            input_ids=input_ids,
            attention_mask=attention_mask
        )
        
        # Use [CLS] token representation (first token)
        pooled_output = outputs.last_hidden_state[:, 0, :]
        
        # Get predictions from both heads (dropout is in the Sequential)
        category_logits = self.category_classifier(pooled_output)
        priority_logits = self.priority_classifier(pooled_output)
        
        return category_logits, priority_logits
    
    def predict(self, input_ids, attention_mask):
        """
        Make predictions with confidence scores
        
        Returns:
            category_pred: Predicted category ID
            category_conf: Category confidence score
            priority_pred: Predicted priority ID
            priority_conf: Priority confidence score
        """
        self.eval()
        with torch.no_grad():
            category_logits, priority_logits = self.forward(input_ids, attention_mask)
            
            # Apply softmax to get probabilities
            category_probs = torch.softmax(category_logits, dim=1)
            priority_probs = torch.softmax(priority_logits, dim=1)
            
            # Get predictions and confidence
            category_conf, category_pred = torch.max(category_probs, dim=1)
            priority_conf, priority_pred = torch.max(priority_probs, dim=1)
            
            return category_pred, category_conf, priority_pred, priority_conf


if __name__ == "__main__":
    # Test model initialization
    print(f"Initializing model: {Config.MODEL_NAME}")
    model = MultiTaskTicketClassifier()
    print(f"Model parameters: {sum(p.numel() for p in model.parameters()):,}")
    print(f"Trainable parameters: {sum(p.numel() for p in model.parameters() if p.requires_grad):,}")
    
    # Test forward pass
    batch_size = 2
    seq_length = 128
    input_ids = torch.randint(0, 1000, (batch_size, seq_length))
    attention_mask = torch.ones(batch_size, seq_length)
    
    category_logits, priority_logits = model(input_ids, attention_mask)
    print(f"\nCategory logits shape: {category_logits.shape}")
    print(f"Priority logits shape: {priority_logits.shape}")
