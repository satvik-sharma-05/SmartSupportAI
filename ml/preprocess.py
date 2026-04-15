"""
Data preprocessing utilities for training
"""
import pandas as pd
from typing import List, Tuple
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.utils import preprocess_text


def load_and_preprocess_data(file_path: str) -> pd.DataFrame:
    """
    Load and preprocess training data from CSV.
    
    Expected CSV format:
    text,category
    "ticket text here","Billing"
    """
    df = pd.read_csv(file_path)
    
    # Validate columns
    required_cols = ['text', 'category']
    if not all(col in df.columns for col in required_cols):
        raise ValueError(f"CSV must contain columns: {required_cols}")
    
    # Remove empty rows
    df = df.dropna(subset=['text', 'category'])
    
    # Preprocess text
    df['cleaned_text'] = df['text'].apply(preprocess_text)
    
    # Remove rows with empty cleaned text
    df = df[df['cleaned_text'].str.len() > 0]
    
    return df


def augment_data(texts: List[str], labels: List[str]) -> Tuple[List[str], List[str]]:
    """
    Simple data augmentation by adding variations.
    """
    augmented_texts = texts.copy()
    augmented_labels = labels.copy()
    
    # Add variations (simple approach)
    for text, label in zip(texts, labels):
        # Add uppercase version
        augmented_texts.append(text.upper())
        augmented_labels.append(label)
    
    return augmented_texts, augmented_labels


if __name__ == "__main__":
    # Example usage
    print("Preprocessing utilities loaded")
    print("Use load_and_preprocess_data('path/to/data.csv') to load your dataset")
