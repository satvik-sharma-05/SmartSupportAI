"""
Data preparation script for SmartSupport AI
Downloads and processes multiple real-world datasets
"""
import pandas as pd
import numpy as np
import re
import os
from typing import List, Tuple
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')


class DatasetPreparer:
    """Prepare and merge multiple support ticket datasets"""
    
    def __init__(self):
        self.data_dir = "data/raw"
        self.processed_dir = "data/processed"
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.processed_dir, exist_ok=True)
        
        # Priority keywords
        self.high_priority_keywords = [
            'urgent', 'critical', 'emergency', 'asap', 'immediately',
            'failed', 'error', 'crash', 'down', 'broken', 'not working',
            'cannot', 'unable', 'blocked', 'stuck', 'lost', 'missing'
        ]
        
        self.medium_priority_keywords = [
            'delay', 'slow', 'issue', 'problem', 'help', 'need',
            'question', 'how to', 'confused', 'unclear'
        ]
        
        # Category mapping for standardization
        self.category_mapping = {
            # Technical variations
            'technical': 'Technical',
            'tech': 'Technical',
            'technical support': 'Technical',
            'technical issue': 'Technical',
            'software': 'Technical',
            'hardware': 'Technical',
            'bug': 'Technical',
            'error': 'Technical',
            'system': 'Technical',
            'network': 'Technical',
            'connectivity': 'Technical',
            'access': 'Technical',
            'login': 'Technical',
            'password': 'Technical',
            
            # Billing variations
            'billing': 'Billing',
            'payment': 'Billing',
            'invoice': 'Billing',
            'charge': 'Billing',
            'refund': 'Billing',
            'subscription': 'Billing',
            'pricing': 'Billing',
            'cost': 'Billing',
            
            # Account variations
            'account': 'Account',
            'profile': 'Account',
            'settings': 'Account',
            'user': 'Account',
            'registration': 'Account',
            'signup': 'Account',
            
            # General variations
            'general': 'General',
            'inquiry': 'General',
            'question': 'General',
            'information': 'General',
            'other': 'General',
            'misc': 'General',
            'miscellaneous': 'General',
        }
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        if not isinstance(text, str):
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^a-zA-Z0-9\s.,!?]', '', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text.strip()
    
    def normalize_category(self, category: str) -> str:
        """Normalize category labels"""
        if not isinstance(category, str):
            return 'General'
        
        category_lower = category.lower().strip()
        
        # Direct mapping
        if category_lower in self.category_mapping:
            return self.category_mapping[category_lower]
        
        # Partial matching
        for key, value in self.category_mapping.items():
            if key in category_lower:
                return value
        
        return 'General'
    
    def assign_priority(self, text: str) -> str:
        """Assign priority based on keywords and sentiment"""
        if not isinstance(text, str):
            return 'Low'
        
        text_lower = text.lower()
        
        # Check for high priority keywords
        high_count = sum(1 for keyword in self.high_priority_keywords if keyword in text_lower)
        if high_count >= 2:
            return 'High'
        
        # Check for medium priority keywords
        medium_count = sum(1 for keyword in self.medium_priority_keywords if keyword in text_lower)
        if medium_count >= 2 or high_count == 1:
            return 'Medium'
        
        # Check for urgency indicators
        if any(word in text_lower for word in ['urgent', 'critical', 'emergency', 'asap']):
            return 'High'
        
        return 'Low'
    
    def load_and_process_datasets(self) -> pd.DataFrame:
        """Load and process all available datasets"""
        print("\n" + "="*60)
        print("DATASET PREPARATION")
        print("="*60)
        
        all_data = []
        
        # Try to load real datasets if available
        dataset_files = [
            'customer_support_tickets.csv',
            'it_service_tickets.csv',
            'support_tickets.csv',
            'complaints.csv'
        ]
        
        for filename in dataset_files:
            filepath = os.path.join(self.data_dir, filename)
            if os.path.exists(filepath):
                try:
                    print(f"\nLoading {filename}...")
                    df = pd.read_csv(filepath)
                    print(f"  Loaded {len(df)} rows")
                    
                    # Process based on file structure
                    processed_df = self.process_dataset(df, filename)
                    if processed_df is not None and len(processed_df) > 0:
                        all_data.append(processed_df)
                        print(f"  Processed {len(processed_df)} valid samples")
                except Exception as e:
                    print(f"  Error loading {filename}: {e}")
        
        # If no real datasets found, exit with error
        if not all_data:
            print("\n" + "="*60)
            print("ERROR: NO REAL DATASETS FOUND")
            print("="*60)
            print("\nThis project uses ONLY real-world datasets.")
            print("\nTo download real datasets:")
            print("1. Install kagglehub: pip install kagglehub")
            print("2. Run: python ml/download_datasets.py")
            print("   OR: python ml/setup_real_datasets.py")
            print("\nDatasets will be downloaded from Kaggle:")
            print("  - suraj520/customer-support-ticket-dataset")
            print("  - adisongoh/it-service-ticket-classification-dataset")
            print("  - namigabbasov/consumer-complaint-dataset")
            return None
        
        # Combine all datasets
        print("\nCombining datasets...")
        combined_df = pd.concat(all_data, ignore_index=True)
        
        # Clean and process
        print("Cleaning text...")
        combined_df['text'] = combined_df['text'].apply(self.clean_text)
        
        # Remove empty texts
        combined_df = combined_df[combined_df['text'].str.len() > 10]
        
        # Remove duplicates
        print("Removing duplicates...")
        before_dedup = len(combined_df)
        combined_df = combined_df.drop_duplicates(subset=['text'])
        print(f"  Removed {before_dedup - len(combined_df)} duplicates")
        
        # Balance dataset if needed
        combined_df = self.balance_dataset(combined_df)
        
        # Save processed dataset
        output_path = os.path.join(self.processed_dir, 'combined_dataset.csv')
        combined_df.to_csv(output_path, index=False)
        print(f"\nSaved processed dataset to {output_path}")
        
        # Print statistics
        self.print_statistics(combined_df)
        
        return combined_df
    
    def process_dataset(self, df: pd.DataFrame, filename: str) -> pd.DataFrame:
        """Process individual dataset based on its structure"""
        processed_data = []
        
        # Try to identify text and category columns
        text_cols = ['text', 'description', 'ticket', 'complaint', 'issue', 'message', 'content']
        category_cols = ['category', 'type', 'label', 'class', 'classification']
        
        text_col = None
        category_col = None
        
        for col in df.columns:
            col_lower = col.lower()
            if any(tc in col_lower for tc in text_cols) and text_col is None:
                text_col = col
            if any(cc in col_lower for cc in category_cols) and category_col is None:
                category_col = col
        
        if text_col is None or category_col is None:
            print(f"  Could not identify columns in {filename}")
            return None
        
        for _, row in df.iterrows():
            text = str(row[text_col])
            category = self.normalize_category(str(row[category_col]))
            priority = self.assign_priority(text)
            
            if len(text) > 10:
                processed_data.append({
                    'text': text,
                    'category': category,
                    'priority': priority
                })
        
        return pd.DataFrame(processed_data)
    
    def balance_dataset(self, df: pd.DataFrame, max_samples_per_class: int = 500) -> pd.DataFrame:
        """Balance dataset by category and priority"""
        print("\nBalancing dataset...")
        
        balanced_dfs = []
        
        # Balance by category
        for category in df['category'].unique():
            category_df = df[df['category'] == category]
            if len(category_df) > max_samples_per_class:
                category_df = category_df.sample(n=max_samples_per_class, random_state=42)
            balanced_dfs.append(category_df)
        
        balanced_df = pd.concat(balanced_dfs, ignore_index=True)
        
        print(f"  Balanced from {len(df)} to {len(balanced_df)} samples")
        
        return balanced_df
    
    def print_statistics(self, df: pd.DataFrame):
        """Print dataset statistics"""
        print("\n" + "="*60)
        print("DATASET STATISTICS")
        print("="*60)
        print(f"\nTotal samples: {len(df)}")
        
        print("\nCategory distribution:")
        print(df['category'].value_counts())
        
        print("\nPriority distribution:")
        print(df['priority'].value_counts())
        
        print("\nText length statistics:")
        df['text_length'] = df['text'].str.len()
        print(f"  Mean: {df['text_length'].mean():.0f} characters")
        print(f"  Median: {df['text_length'].median():.0f} characters")
        print(f"  Min: {df['text_length'].min():.0f} characters")
        print(f"  Max: {df['text_length'].max():.0f} characters")


def main():
    """Main function to prepare datasets"""
    preparer = DatasetPreparer()
    df = preparer.load_and_process_datasets()
    
    print("\n" + "="*60)
    print("DATASET PREPARATION COMPLETE")
    print("="*60)
    print(f"\nProcessed dataset saved to: data/processed/combined_dataset.csv")
    print(f"Total samples: {len(df)}")
    print("\nNext step: Run training script")
    print("  python ml/train_advanced.py")


if __name__ == "__main__":
    main()
