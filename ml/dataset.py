"""
Dataset creation and preprocessing for SmartSupport AI
"""
import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer
from sklearn.model_selection import train_test_split
from typing import Dict, List, Tuple
import numpy as np

from ml.config import Config


class TicketDataset(Dataset):
    """PyTorch Dataset for support tickets"""
    
    def __init__(self, texts: List[str], categories: List[int], 
                 priorities: List[int], tokenizer, max_length: int):
        self.texts = texts
        self.categories = categories
        self.priorities = priorities
        self.tokenizer = tokenizer
        self.max_length = max_length
    
    def __len__(self):
        return len(self.texts)
    
    def __getitem__(self, idx):
        text = str(self.texts[idx])
        category = self.categories[idx]
        priority = self.priorities[idx]
        
        # Tokenize
        encoding = self.tokenizer(
            text,
            add_special_tokens=True,
            max_length=self.max_length,
            padding='max_length',
            truncation=True,
            return_attention_mask=True,
            return_tensors='pt'
        )
        
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'category': torch.tensor(category, dtype=torch.long),
            'priority': torch.tensor(priority, dtype=torch.long)
        }


def create_sample_dataset() -> pd.DataFrame:
    """
    Create a comprehensive sample dataset for training.
    In production, replace with real ticket data.
    """
    # Simplified dataset with exact counts
    texts = []
    categories = []
    priorities = []
    
    # Billing tickets (12 total)
    billing_tickets = [
        ("URGENT: I was charged twice for my subscription this month", "High"),
        ("My credit card was charged but I didn't authorize this payment", "High"),
        ("Emergency: Payment failed but money was deducted from my account", "High"),
        ("Critical billing issue - overcharged by $500", "High"),
        ("I need a refund for last month's payment", "Medium"),
        ("The invoice amount seems incorrect", "Medium"),
        ("Can I get a receipt for my recent purchase", "Medium"),
        ("Billing cycle date is wrong on my account", "Medium"),
        ("What payment methods do you accept", "Low"),
        ("How do I update my billing information", "Low"),
        ("When will I receive my next invoice", "Low"),
        ("Can I change my payment plan", "Low"),
    ]
    
    for text, priority in billing_tickets:
        texts.append(text)
        categories.append("Billing")
        priorities.append(priority)
    
    # Technical tickets (12 total)
    technical_tickets = [
        ("URGENT: Cannot login to my account at all", "High"),
        ("Critical: App crashes immediately when I open it", "High"),
        ("Emergency: Getting error 500 on all pages", "High"),
        ("System is completely down, cannot access anything", "High"),
        ("App is running very slow lately", "Medium"),
        ("Getting timeout errors occasionally", "Medium"),
        ("Integration with API is not working properly", "Medium"),
        ("Upload feature is broken", "Medium"),
        ("Minor UI glitch on the settings page", "Low"),
        ("Feature request: Add dark mode", "Low"),
        ("How do I use the export function", "Low"),
        ("Is there a way to customize the interface", "Low"),
    ]
    
    for text, priority in technical_tickets:
        texts.append(text)
        categories.append("Technical")
        priorities.append(priority)
    
    # Account tickets (12 total)
    account_tickets = [
        ("URGENT: Account locked and cannot access", "High"),
        ("Cannot verify my email, locked out of account", "High"),
        ("Critical: Someone else accessed my account", "High"),
        ("Emergency: Need to recover my account immediately", "High"),
        ("Need to update my email address", "Medium"),
        ("How do I change my password", "Medium"),
        ("Want to add team members to my account", "Medium"),
        ("Need to update my profile information", "Medium"),
        ("How do I change my username", "Low"),
        ("Can I customize my profile picture", "Low"),
        ("What information is visible to other users", "Low"),
        ("How do I manage notification settings", "Low"),
    ]
    
    for text, priority in account_tickets:
        texts.append(text)
        categories.append("Account")
        priorities.append(priority)
    
    # General tickets (12 total)
    general_tickets = [
        ("URGENT: Need immediate assistance with setup", "High"),
        ("Critical question about data security", "High"),
        ("How does your service work", "Medium"),
        ("What features are included in the pro plan", "Medium"),
        ("Need help getting started with the platform", "Medium"),
        ("Can you explain the pricing structure", "Medium"),
        ("Do you offer student discounts", "Low"),
        ("Where can I find the documentation", "Low"),
        ("What are your business hours", "Low"),
        ("Is there a mobile app available", "Low"),
        ("How do I contact the sales team", "Low"),
        ("What integrations do you support", "Low"),
    ]
    
    for text, priority in general_tickets:
        texts.append(text)
        categories.append("General")
        priorities.append(priority)
    
    data = {
        'text': texts,
        'category': categories,
        'priority': priorities
    }
    
    return pd.DataFrame(data)


def prepare_data(df: pd.DataFrame, tokenizer) -> Tuple[DataLoader, DataLoader, DataLoader]:
    """
    Prepare train, validation, and test dataloaders
    """
    # Convert categories and priorities to IDs
    df['category_id'] = df['category'].apply(Config.get_category_id)
    df['priority_id'] = df['priority'].apply(Config.get_priority_id)
    
    # Split data
    train_df, temp_df = train_test_split(
        df, test_size=(Config.VAL_SPLIT + Config.TEST_SPLIT),
        random_state=42, stratify=df['category']
    )
    
    val_df, test_df = train_test_split(
        temp_df, test_size=Config.TEST_SPLIT / (Config.VAL_SPLIT + Config.TEST_SPLIT),
        random_state=42, stratify=temp_df['category']
    )
    
    print(f"Train samples: {len(train_df)}")
    print(f"Validation samples: {len(val_df)}")
    print(f"Test samples: {len(test_df)}")
    
    # Create datasets
    train_dataset = TicketDataset(
        train_df['text'].tolist(),
        train_df['category_id'].tolist(),
        train_df['priority_id'].tolist(),
        tokenizer,
        Config.MAX_LENGTH
    )
    
    val_dataset = TicketDataset(
        val_df['text'].tolist(),
        val_df['category_id'].tolist(),
        val_df['priority_id'].tolist(),
        tokenizer,
        Config.MAX_LENGTH
    )
    
    test_dataset = TicketDataset(
        test_df['text'].tolist(),
        test_df['category_id'].tolist(),
        test_df['priority_id'].tolist(),
        tokenizer,
        Config.MAX_LENGTH
    )
    
    # Create dataloaders
    train_loader = DataLoader(
        train_dataset,
        batch_size=Config.BATCH_SIZE,
        shuffle=True
    )
    
    val_loader = DataLoader(
        val_dataset,
        batch_size=Config.BATCH_SIZE,
        shuffle=False
    )
    
    test_loader = DataLoader(
        test_dataset,
        batch_size=Config.BATCH_SIZE,
        shuffle=False
    )
    
    return train_loader, val_loader, test_loader


if __name__ == "__main__":
    # Test dataset creation
    df = create_sample_dataset()
    print(f"Created dataset with {len(df)} samples")
    print(f"\nCategory distribution:")
    print(df['category'].value_counts())
    print(f"\nPriority distribution:")
    print(df['priority'].value_counts())
