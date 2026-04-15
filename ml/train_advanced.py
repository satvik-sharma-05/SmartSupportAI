"""
Advanced training script for SmartSupport AI
Uses real-world datasets and state-of-the-art transformer models
"""
import pandas as pd
import torch
import torch.nn as nn
from torch.optim import AdamW
from transformers import AutoTokenizer, get_linear_schedule_with_warmup
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, classification_report
import numpy as np
import os
from tqdm import tqdm
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ml.config import Config
from ml.model import MultiTaskTicketClassifier
from ml.dataset import TicketDataset, prepare_data


class AdvancedTrainer:
    """Advanced trainer with real-world data"""
    
    def __init__(self, model, train_loader, val_loader, test_loader):
        self.model = model.to(Config.DEVICE)
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.test_loader = test_loader
        
        # Loss functions
        self.category_criterion = nn.CrossEntropyLoss()
        self.priority_criterion = nn.CrossEntropyLoss()
        
        # Optimizer with weight decay
        self.optimizer = AdamW(
            model.parameters(),
            lr=Config.LEARNING_RATE,
            weight_decay=Config.WEIGHT_DECAY,
            eps=1e-8
        )
        
        # Learning rate scheduler
        total_steps = len(train_loader) * Config.NUM_EPOCHS
        self.scheduler = get_linear_schedule_with_warmup(
            self.optimizer,
            num_warmup_steps=Config.WARMUP_STEPS,
            num_training_steps=total_steps
        )
        
        self.best_val_loss = float('inf')
        self.best_val_acc = 0.0
    
    def train_epoch(self, epoch):
        """Train for one epoch"""
        self.model.train()
        total_loss = 0
        category_correct = 0
        priority_correct = 0
        total_samples = 0
        
        progress_bar = tqdm(self.train_loader, desc=f"Epoch {epoch+1}/{Config.NUM_EPOCHS}")
        
        for batch in progress_bar:
            # Move to device
            input_ids = batch['input_ids'].to(Config.DEVICE)
            attention_mask = batch['attention_mask'].to(Config.DEVICE)
            category_labels = batch['category'].to(Config.DEVICE)
            priority_labels = batch['priority'].to(Config.DEVICE)
            
            # Forward pass
            category_logits, priority_logits = self.model(input_ids, attention_mask)
            
            # Calculate losses
            category_loss = self.category_criterion(category_logits, category_labels)
            priority_loss = self.priority_criterion(priority_logits, priority_labels)
            
            # Combined loss
            loss = (Config.CATEGORY_WEIGHT * category_loss + 
                   Config.PRIORITY_WEIGHT * priority_loss)
            
            # Backward pass
            self.optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), 1.0)
            self.optimizer.step()
            self.scheduler.step()
            
            # Calculate accuracy
            category_preds = torch.argmax(category_logits, dim=1)
            priority_preds = torch.argmax(priority_logits, dim=1)
            
            category_correct += (category_preds == category_labels).sum().item()
            priority_correct += (priority_preds == priority_labels).sum().item()
            total_samples += category_labels.size(0)
            total_loss += loss.item()
            
            # Update progress bar
            progress_bar.set_postfix({
                'loss': f'{loss.item():.4f}',
                'cat_acc': f'{category_correct/total_samples:.4f}',
                'pri_acc': f'{priority_correct/total_samples:.4f}'
            })
        
        avg_loss = total_loss / len(self.train_loader)
        category_acc = category_correct / total_samples
        priority_acc = priority_correct / total_samples
        
        return avg_loss, category_acc, priority_acc
    
    def validate(self):
        """Validate the model"""
        self.model.eval()
        total_loss = 0
        category_preds_all = []
        priority_preds_all = []
        category_labels_all = []
        priority_labels_all = []
        
        with torch.no_grad():
            for batch in self.val_loader:
                input_ids = batch['input_ids'].to(Config.DEVICE)
                attention_mask = batch['attention_mask'].to(Config.DEVICE)
                category_labels = batch['category'].to(Config.DEVICE)
                priority_labels = batch['priority'].to(Config.DEVICE)
                
                category_logits, priority_logits = self.model(input_ids, attention_mask)
                
                category_loss = self.category_criterion(category_logits, category_labels)
                priority_loss = self.priority_criterion(priority_logits, priority_labels)
                loss = Config.CATEGORY_WEIGHT * category_loss + Config.PRIORITY_WEIGHT * priority_loss
                
                total_loss += loss.item()
                
                category_preds = torch.argmax(category_logits, dim=1)
                priority_preds = torch.argmax(priority_logits, dim=1)
                
                category_preds_all.extend(category_preds.cpu().numpy())
                priority_preds_all.extend(priority_preds.cpu().numpy())
                category_labels_all.extend(category_labels.cpu().numpy())
                priority_labels_all.extend(priority_labels.cpu().numpy())
        
        avg_loss = total_loss / len(self.val_loader)
        category_acc = accuracy_score(category_labels_all, category_preds_all)
        priority_acc = accuracy_score(priority_labels_all, priority_preds_all)
        
        return avg_loss, category_acc, priority_acc
    
    def test(self):
        """Test the model and return detailed metrics"""
        self.model.eval()
        category_preds_all = []
        priority_preds_all = []
        category_labels_all = []
        priority_labels_all = []
        
        with torch.no_grad():
            for batch in self.test_loader:
                input_ids = batch['input_ids'].to(Config.DEVICE)
                attention_mask = batch['attention_mask'].to(Config.DEVICE)
                category_labels = batch['category'].to(Config.DEVICE)
                priority_labels = batch['priority'].to(Config.DEVICE)
                
                category_logits, priority_logits = self.model(input_ids, attention_mask)
                
                category_preds = torch.argmax(category_logits, dim=1)
                priority_preds = torch.argmax(priority_logits, dim=1)
                
                category_preds_all.extend(category_preds.cpu().numpy())
                priority_preds_all.extend(priority_preds.cpu().numpy())
                category_labels_all.extend(category_labels.cpu().numpy())
                priority_labels_all.extend(priority_labels.cpu().numpy())
        
        # Calculate metrics
        print("\n" + "="*60)
        print("CATEGORY CLASSIFICATION METRICS")
        print("="*60)
        print(classification_report(
            category_labels_all, 
            category_preds_all,
            target_names=Config.CATEGORIES,
            digits=4
        ))
        
        print("\n" + "="*60)
        print("PRIORITY CLASSIFICATION METRICS")
        print("="*60)
        print(classification_report(
            priority_labels_all,
            priority_preds_all,
            target_names=Config.PRIORITIES,
            digits=4
        ))
        
        return category_preds_all, priority_preds_all
    
    def train(self):
        """Full training loop"""
        print("\n" + "="*60)
        print("STARTING TRAINING")
        print("="*60)
        print(f"Device: {Config.DEVICE}")
        print(f"Model: {Config.MODEL_NAME}")
        print(f"Epochs: {Config.NUM_EPOCHS}")
        print(f"Batch size: {Config.BATCH_SIZE}")
        print(f"Learning rate: {Config.LEARNING_RATE}")
        
        for epoch in range(Config.NUM_EPOCHS):
            # Train
            train_loss, train_cat_acc, train_pri_acc = self.train_epoch(epoch)
            
            # Validate
            val_loss, val_cat_acc, val_pri_acc = self.validate()
            
            print(f"\nEpoch {epoch+1}/{Config.NUM_EPOCHS}")
            print(f"Train Loss: {train_loss:.4f} | Val Loss: {val_loss:.4f}")
            print(f"Train Cat Acc: {train_cat_acc:.4f} | Val Cat Acc: {val_cat_acc:.4f}")
            print(f"Train Pri Acc: {train_pri_acc:.4f} | Val Pri Acc: {val_pri_acc:.4f}")
            
            # Save best model
            avg_val_acc = (val_cat_acc + val_pri_acc) / 2
            if avg_val_acc > self.best_val_acc:
                self.best_val_acc = avg_val_acc
                self.save_model()
                print(f"✓ Model saved (best avg accuracy: {avg_val_acc:.4f})")
        
        print("\n" + "="*60)
        print("TRAINING COMPLETE")
        print("="*60)
        
        # Test on test set
        print("\nEvaluating on test set...")
        self.test()
    
    def save_model(self):
        """Save model and tokenizer"""
        os.makedirs(Config.MODEL_SAVE_PATH, exist_ok=True)
        torch.save(self.model.state_dict(), f"{Config.MODEL_SAVE_PATH}/model.pt")


def main():
    """Main training function"""
    print("="*60)
    print("SmartSupport AI - Advanced Training")
    print("="*60)
    
    # Check for processed dataset
    dataset_path = "data/processed/combined_dataset.csv"
    
    if not os.path.exists(dataset_path):
        print("\n❌ Processed dataset not found!")
        print("\nPlease run data preparation first:")
        print("  python ml/data_preparation.py")
        print("\nThis will:")
        print("  1. Download/load real-world datasets")
        print("  2. Clean and process the data")
        print("  3. Create a unified dataset")
        return
    
    # Load dataset
    print("\n[1/5] Loading processed dataset...")
    df = pd.read_csv(dataset_path)
    print(f"✓ Loaded {len(df)} samples")
    print(f"\nCategory distribution:")
    print(df['category'].value_counts())
    print(f"\nPriority distribution:")
    print(df['priority'].value_counts())
    
    # Load tokenizer
    print("\n[2/5] Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(Config.MODEL_NAME)
    print(f"✓ Loaded tokenizer: {Config.MODEL_NAME}")
    
    # Prepare data
    print("\n[3/5] Preparing dataloaders...")
    train_loader, val_loader, test_loader = prepare_data(df, tokenizer)
    print("✓ Dataloaders ready")
    
    # Initialize model
    print("\n[4/5] Initializing model...")
    model = MultiTaskTicketClassifier(Config.MODEL_NAME)
    total_params = sum(p.numel() for p in model.parameters())
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"✓ Model initialized")
    print(f"  Total parameters: {total_params:,}")
    print(f"  Trainable parameters: {trainable_params:,}")
    
    # Train
    print("\n[5/5] Training model...")
    trainer = AdvancedTrainer(model, train_loader, val_loader, test_loader)
    trainer.train()
    
    # Save tokenizer
    print("\n[SAVE] Saving tokenizer...")
    os.makedirs(Config.TOKENIZER_SAVE_PATH, exist_ok=True)
    tokenizer.save_pretrained(Config.TOKENIZER_SAVE_PATH)
    print(f"✓ Tokenizer saved to {Config.TOKENIZER_SAVE_PATH}")
    
    print("\n" + "="*60)
    print("ALL DONE!")
    print("="*60)
    print(f"\nModel saved at: {Config.MODEL_SAVE_PATH}")
    print(f"Tokenizer saved at: {Config.TOKENIZER_SAVE_PATH}")
    print("\nNext steps:")
    print("1. Update .env with MongoDB credentials (optional)")
    print("2. Run: uvicorn app.main:app --reload")
    print("3. Test API at: http://localhost:8000/docs")


if __name__ == "__main__":
    main()
