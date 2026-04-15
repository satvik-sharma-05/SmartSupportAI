"""
Fast training script for CPU - uses DistilBERT (smaller, faster)
"""
import torch
import torch.nn as nn
from torch.optim import AdamW
from transformers import AutoTokenizer, AutoModel, get_linear_schedule_with_warmup
from sklearn.metrics import accuracy_score, classification_report
import numpy as np
import os
from tqdm import tqdm
import pandas as pd

# Simplified config for fast training
class FastConfig:
    MODEL_NAME = "distilbert-base-uncased"  # Smaller, faster model
    MAX_LENGTH = 128  # Shorter sequences
    BATCH_SIZE = 32  # Larger batches
    LEARNING_RATE = 3e-5
    NUM_EPOCHS = 3  # Fewer epochs
    WARMUP_STEPS = 100
    DEVICE = torch.device('cpu')
    CATEGORY_WEIGHT = 0.6
    PRIORITY_WEIGHT = 0.4
    
    CATEGORIES = ['Billing', 'Technical', 'Account', 'General']
    PRIORITIES = ['High', 'Medium', 'Low']
    
    NUM_CATEGORIES = len(CATEGORIES)
    NUM_PRIORITIES = len(PRIORITIES)


class FastTicketClassifier(nn.Module):
    """Lightweight classifier for CPU training"""
    
    def __init__(self):
        super().__init__()
        self.transformer = AutoModel.from_pretrained(FastConfig.MODEL_NAME)
        hidden_size = self.transformer.config.hidden_size
        
        # Simpler classification heads
        self.category_classifier = nn.Sequential(
            nn.Dropout(0.1),
            nn.Linear(hidden_size, FastConfig.NUM_CATEGORIES)
        )
        
        self.priority_classifier = nn.Sequential(
            nn.Dropout(0.1),
            nn.Linear(hidden_size, FastConfig.NUM_PRIORITIES)
        )
    
    def forward(self, input_ids, attention_mask):
        outputs = self.transformer(input_ids=input_ids, attention_mask=attention_mask)
        pooled_output = outputs.last_hidden_state[:, 0, :]  # CLS token
        
        category_logits = self.category_classifier(pooled_output)
        priority_logits = self.priority_classifier(pooled_output)
        
        return category_logits, priority_logits


def load_data():
    """Load processed dataset"""
    print("\n[1/6] Loading dataset...")
    df = pd.read_csv('data/processed/combined_dataset.csv')
    print(f"✓ Loaded {len(df)} samples")
    
    # Map labels to indices
    df['category_idx'] = df['category'].map({cat: idx for idx, cat in enumerate(FastConfig.CATEGORIES)})
    df['priority_idx'] = df['priority'].map({pri: idx for idx, pri in enumerate(FastConfig.PRIORITIES)})
    
    # Split data
    from sklearn.model_selection import train_test_split
    train_df, temp_df = train_test_split(df, test_size=0.3, random_state=42, stratify=df['category'])
    val_df, test_df = train_test_split(temp_df, test_size=0.5, random_state=42, stratify=temp_df['category'])
    
    print(f"  Train: {len(train_df)}, Val: {len(val_df)}, Test: {len(test_df)}")
    
    return train_df, val_df, test_df


def create_dataloader(df, tokenizer, batch_size, shuffle=True):
    """Create dataloader"""
    texts = df['text'].tolist()
    categories = df['category_idx'].tolist()
    priorities = df['priority_idx'].tolist()
    
    encodings = tokenizer(
        texts,
        truncation=True,
        padding=True,
        max_length=FastConfig.MAX_LENGTH,
        return_tensors='pt'
    )
    
    dataset = torch.utils.data.TensorDataset(
        encodings['input_ids'],
        encodings['attention_mask'],
        torch.tensor(categories),
        torch.tensor(priorities)
    )
    
    return torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)


def train_epoch(model, dataloader, optimizer, scheduler, criterion):
    """Train one epoch"""
    model.train()
    total_loss = 0
    cat_correct = 0
    pri_correct = 0
    total = 0
    
    for batch in tqdm(dataloader, desc="Training"):
        input_ids, attention_mask, cat_labels, pri_labels = batch
        
        optimizer.zero_grad()
        
        cat_logits, pri_logits = model(input_ids, attention_mask)
        
        cat_loss = criterion(cat_logits, cat_labels)
        pri_loss = criterion(pri_logits, pri_labels)
        
        loss = FastConfig.CATEGORY_WEIGHT * cat_loss + FastConfig.PRIORITY_WEIGHT * pri_loss
        
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        scheduler.step()
        
        total_loss += loss.item()
        cat_correct += (cat_logits.argmax(1) == cat_labels).sum().item()
        pri_correct += (pri_logits.argmax(1) == pri_labels).sum().item()
        total += len(cat_labels)
    
    return total_loss / len(dataloader), cat_correct / total, pri_correct / total


def evaluate(model, dataloader, criterion):
    """Evaluate model"""
    model.eval()
    total_loss = 0
    cat_correct = 0
    pri_correct = 0
    total = 0
    
    with torch.no_grad():
        for batch in dataloader:
            input_ids, attention_mask, cat_labels, pri_labels = batch
            
            cat_logits, pri_logits = model(input_ids, attention_mask)
            
            cat_loss = criterion(cat_logits, cat_labels)
            pri_loss = criterion(pri_logits, pri_labels)
            
            loss = FastConfig.CATEGORY_WEIGHT * cat_loss + FastConfig.PRIORITY_WEIGHT * pri_loss
            
            total_loss += loss.item()
            cat_correct += (cat_logits.argmax(1) == cat_labels).sum().item()
            pri_correct += (pri_logits.argmax(1) == pri_labels).sum().item()
            total += len(cat_labels)
    
    return total_loss / len(dataloader), cat_correct / total, pri_correct / total


def main():
    print("="*60)
    print("SmartSupport AI - Fast Training (CPU Optimized)")
    print("="*60)
    
    # Load data
    train_df, val_df, test_df = load_data()
    
    # Load tokenizer
    print("\n[2/6] Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(FastConfig.MODEL_NAME)
    print(f"✓ Loaded: {FastConfig.MODEL_NAME}")
    
    # Create dataloaders
    print("\n[3/6] Creating dataloaders...")
    train_loader = create_dataloader(train_df, tokenizer, FastConfig.BATCH_SIZE, shuffle=True)
    val_loader = create_dataloader(val_df, tokenizer, FastConfig.BATCH_SIZE, shuffle=False)
    test_loader = create_dataloader(test_df, tokenizer, FastConfig.BATCH_SIZE, shuffle=False)
    print("✓ Dataloaders ready")
    
    # Initialize model
    print("\n[4/6] Initializing model...")
    model = FastTicketClassifier()
    print(f"✓ Model initialized")
    print(f"  Parameters: {sum(p.numel() for p in model.parameters()):,}")
    
    # Setup training
    criterion = nn.CrossEntropyLoss()
    optimizer = AdamW(model.parameters(), lr=FastConfig.LEARNING_RATE)
    total_steps = len(train_loader) * FastConfig.NUM_EPOCHS
    scheduler = get_linear_schedule_with_warmup(optimizer, FastConfig.WARMUP_STEPS, total_steps)
    
    # Training loop
    print("\n[5/6] Training...")
    print("="*60)
    best_val_acc = 0
    
    for epoch in range(FastConfig.NUM_EPOCHS):
        print(f"\nEpoch {epoch+1}/{FastConfig.NUM_EPOCHS}")
        
        train_loss, train_cat_acc, train_pri_acc = train_epoch(model, train_loader, optimizer, scheduler, criterion)
        val_loss, val_cat_acc, val_pri_acc = evaluate(model, val_loader, criterion)
        
        print(f"  Train Loss: {train_loss:.4f} | Cat Acc: {train_cat_acc:.4f} | Pri Acc: {train_pri_acc:.4f}")
        print(f"  Val Loss: {val_loss:.4f} | Cat Acc: {val_cat_acc:.4f} | Pri Acc: {val_pri_acc:.4f}")
        
        if val_cat_acc > best_val_acc:
            best_val_acc = val_cat_acc
            torch.save({
                'model_state_dict': model.state_dict(),
                'tokenizer_name': FastConfig.MODEL_NAME,
                'categories': FastConfig.CATEGORIES,
                'priorities': FastConfig.PRIORITIES
            }, 'models/smartsupport_model/model_fast.pt')
            print("  ✓ Saved best model")
    
    # Test evaluation
    print("\n[6/6] Testing...")
    test_loss, test_cat_acc, test_pri_acc = evaluate(model, test_loader, criterion)
    print(f"  Test Loss: {test_loss:.4f}")
    print(f"  Category Accuracy: {test_cat_acc:.4f}")
    print(f"  Priority Accuracy: {test_pri_acc:.4f}")
    
    print("\n" + "="*60)
    print("TRAINING COMPLETE!")
    print("="*60)
    print(f"Model saved to: models/smartsupport_model/model_fast.pt")
    print(f"Best validation accuracy: {best_val_acc:.4f}")


if __name__ == "__main__":
    main()
