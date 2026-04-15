"""
Download real-world datasets from multiple sources
Supports both Kaggle and Hugging Face datasets
"""
import os
import pandas as pd
import numpy as np
import re
from typing import List, Dict
import warnings
warnings.filterwarnings('ignore')


class RealDatasetDownloader:
    """Download and process real-world support ticket datasets"""
    
    def __init__(self):
        self.data_dir = "data/raw"
        self.processed_dir = "data/processed"
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.processed_dir, exist_ok=True)
        
        # Priority keywords
        self.high_priority_keywords = [
            'urgent', 'critical', 'emergency', 'asap', 'immediately',
            'failed', 'error', 'crash', 'down', 'broken', 'not working',
            'cannot', 'unable', 'blocked', 'stuck', 'lost', 'missing',
            'severe', 'major', 'outage', 'dead', 'frozen', 'critical'
        ]
        
        self.medium_priority_keywords = [
            'delay', 'slow', 'issue', 'problem', 'help', 'need',
            'question', 'how to', 'confused', 'unclear', 'intermittent',
            'sometimes', 'occasionally', 'minor'
        ]
        
        # Category mapping
        self.category_mapping = {
            'technical': 'Technical', 'tech': 'Technical', 'software': 'Technical',
            'hardware': 'Technical', 'bug': 'Technical', 'error': 'Technical',
            'system': 'Technical', 'network': 'Technical', 'connectivity': 'Technical',
            'access': 'Technical', 'login': 'Technical', 'password': 'Technical',
            'it': 'Technical', 'computer': 'Technical', 'device': 'Technical',
            'billing': 'Billing', 'payment': 'Billing', 'invoice': 'Billing',
            'charge': 'Billing', 'refund': 'Billing', 'subscription': 'Billing',
            'pricing': 'Billing', 'cost': 'Billing', 'money': 'Billing',
            'account': 'Account', 'profile': 'Account', 'settings': 'Account',
            'user': 'Account', 'registration': 'Account', 'signup': 'Account',
            'general': 'General', 'inquiry': 'General', 'question': 'General',
            'other': 'General', 'misc': 'General',
        }
    
    def download_from_huggingface(self) -> Dict[str, pd.DataFrame]:
        """Download datasets from Hugging Face"""
        print("\n" + "="*60)
        print("DOWNLOADING FROM HUGGING FACE")
        print("="*60)
        
        datasets = {}
        
        try:
            from datasets import load_dataset
            
            # Dataset 1: Customer Support Tickets
            print("\nDataset 1: Customer Support Tickets...")
            try:
                hf_dataset = load_dataset("Tobi-Bueck/customer-support-tickets", split="train")
                df1 = pd.DataFrame(hf_dataset)
                print(f"✓ Downloaded {len(df1)} records")
                print(f"  Columns: {list(df1.columns)}")
                datasets['hf_support_tickets'] = df1
            except Exception as e:
                print(f"✗ Failed: {e}")
            
            # Dataset 2: PIISA Dataset (Customer Service)
            print("\nDataset 2: PIISA Customer Service...")
            try:
                hf_dataset = load_dataset("PIISA/dataset", split="train")
                df2 = pd.DataFrame(hf_dataset)
                # Sample if too large
                if len(df2) > 10000:
                    df2 = df2.sample(n=10000, random_state=42)
                print(f"✓ Downloaded {len(df2)} records")
                print(f"  Columns: {list(df2.columns)}")
                datasets['piisa_dataset'] = df2
            except Exception as e:
                print(f"✗ Failed: {e}")
            
            # Dataset 3: Kaggle Customer Service (on HF)
            print("\nDataset 3: Kaggle Customer Service (HF Mirror)...")
            try:
                hf_dataset = load_dataset("chiapudding/kaggle-customer-service", split="train")
                df3 = pd.DataFrame(hf_dataset)
                if len(df3) > 5000:
                    df3 = df3.sample(n=5000, random_state=42)
                print(f"✓ Downloaded {len(df3)} records")
                print(f"  Columns: {list(df3.columns)}")
                datasets['kaggle_customer_service'] = df3
            except Exception as e:
                print(f"✗ Failed: {e}")
                
        except ImportError:
            print("✗ Hugging Face datasets library not installed")
            print("  Install with: pip install datasets")
        
        return datasets
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        if not isinstance(text, str) or pd.isna(text):
            return ""
        
        text = text.lower()
        text = re.sub(r'http\S+|www\S+|https\S+', '', text)
        text = re.sub(r'\S+@\S+', '', text)
        text = re.sub(r'[^a-zA-Z0-9\s.,!?-]', '', text)
        text = ' '.join(text.split())
        
        return text.strip()
    
    def normalize_category(self, category: str, text: str = "") -> str:
        """Normalize category labels"""
        if not isinstance(category, str) or pd.isna(category):
            # Infer from text
            if text:
                text_lower = text.lower()
                if any(w in text_lower for w in ['payment', 'billing', 'charge', 'invoice', 'refund']):
                    return 'Billing'
                elif any(w in text_lower for w in ['error', 'bug', 'crash', 'technical', 'system', 'network']):
                    return 'Technical'
                elif any(w in text_lower for w in ['account', 'profile', 'login', 'password', 'registration']):
                    return 'Account'
            return 'General'
        
        category_lower = category.lower().strip()
        
        # Direct mapping
        if category_lower in self.category_mapping:
            return self.category_mapping[category_lower]
        
        # Partial matching
        for key, value in self.category_mapping.items():
            if key in category_lower:
                return value
        
        # Keyword inference
        if any(w in category_lower for w in ['tech', 'software', 'hardware', 'system', 'it']):
            return 'Technical'
        elif any(w in category_lower for w in ['bill', 'pay', 'money', 'charge', 'invoice']):
            return 'Billing'
        elif any(w in category_lower for w in ['account', 'user', 'profile', 'login']):
            return 'Account'
        
        return 'General'
    
    def assign_priority(self, text: str) -> str:
        """Assign priority based on keywords"""
        if not isinstance(text, str) or pd.isna(text):
            return 'Low'
        
        text_lower = text.lower()
        
        # High priority
        high_count = sum(1 for kw in self.high_priority_keywords if kw in text_lower)
        if high_count >= 2 or any(w in text_lower for w in ['urgent', 'critical', 'emergency', 'asap']):
            return 'High'
        
        # Medium priority
        medium_count = sum(1 for kw in self.medium_priority_keywords if kw in text_lower)
        if medium_count >= 2 or high_count == 1:
            return 'Medium'
        
        return 'Low'
    
    def process_dataset(self, df: pd.DataFrame, dataset_name: str) -> pd.DataFrame:
        """Process individual dataset"""
        print(f"\nProcessing {dataset_name}...")
        print(f"  Shape: {df.shape}")
        print(f"  Columns: {list(df.columns)}")
        
        processed_data = []
        
        # Identify columns
        text_col = self.identify_column(df, [
            'text', 'description', 'ticket', 'complaint', 'issue', 
            'message', 'content', 'summary', 'title', 'query', 
            'ticket description', 'ticket subject', 'customer message'
        ])
        
        category_col = self.identify_column(df, [
            'category', 'type', 'label', 'class', 'classification', 
            'product', 'issue', 'ticket type', 'ticket category'
        ])
        
        if text_col is None:
            print(f"  ✗ No text column found")
            return pd.DataFrame()
        
        print(f"  Text: {text_col}")
        print(f"  Category: {category_col if category_col else 'None (will infer)'}")
        
        # Process rows
        for idx, row in df.iterrows():
            text = str(row[text_col]) if text_col else ""
            text_clean = self.clean_text(text)
            
            if len(text_clean) < 15:
                continue
            
            # Get category
            if category_col:
                category = self.normalize_category(str(row[category_col]), text_clean)
            else:
                category = self.normalize_category("", text_clean)
            
            # Assign priority
            priority = self.assign_priority(text_clean)
            
            processed_data.append({
                'text': text_clean,
                'category': category,
                'priority': priority,
                'source': dataset_name
            })
        
        result_df = pd.DataFrame(processed_data)
        print(f"  ✓ Processed {len(result_df)} samples")
        
        return result_df
    
    def identify_column(self, df: pd.DataFrame, possible_names: List[str]) -> str:
        """Identify column by matching possible names"""
        for col in df.columns:
            col_lower = col.lower()
            for name in possible_names:
                if name in col_lower or col_lower in name:
                    return col
        return None
    
    def balance_dataset(self, df: pd.DataFrame, samples_per_category: int = 1000) -> pd.DataFrame:
        """Balance dataset by category"""
        print("\nBalancing dataset...")
        
        balanced_dfs = []
        for category in df['category'].unique():
            category_df = df[df['category'] == category]
            
            if len(category_df) > samples_per_category:
                category_df = category_df.sample(n=samples_per_category, random_state=42)
            
            balanced_dfs.append(category_df)
            print(f"  {category}: {len(category_df)} samples")
        
        balanced_df = pd.concat(balanced_dfs, ignore_index=True)
        return balanced_df
    
    def print_statistics(self, df: pd.DataFrame):
        """Print dataset statistics"""
        print("\n" + "="*60)
        print("FINAL DATASET STATISTICS")
        print("="*60)
        print(f"\nTotal samples: {len(df)}")
        
        print("\nCategory distribution:")
        for cat, count in df['category'].value_counts().items():
            print(f"  {cat}: {count} ({count/len(df)*100:.1f}%)")
        
        print("\nPriority distribution:")
        for pri, count in df['priority'].value_counts().items():
            print(f"  {pri}: {count} ({count/len(df)*100:.1f}%)")
        
        if 'source' in df.columns:
            print("\nSource distribution:")
            for src, count in df['source'].value_counts().items():
                print(f"  {src}: {count}")
        
        print("\nText length statistics:")
        df['text_length'] = df['text'].str.len()
        print(f"  Mean: {df['text_length'].mean():.0f} chars")
        print(f"  Median: {df['text_length'].median():.0f} chars")
        print(f"  Min: {df['text_length'].min():.0f} chars")
        print(f"  Max: {df['text_length'].max():.0f} chars")
        
        print("\nSample records:")
        for idx, row in df.sample(n=min(5, len(df))).iterrows():
            print(f"\n  [{row['category']}] [{row['priority']}]")
            print(f"  {row['text'][:120]}...")
    
    def run(self):
        """Main execution"""
        print("\n" + "="*60)
        print("REAL DATASET DOWNLOADER")
        print("SmartSupport AI - Production Dataset Preparation")
        print("="*60)
        
        # Download from Hugging Face
        datasets = self.download_from_huggingface()
        
        if not datasets:
            print("\n✗ No datasets downloaded")
            print("\nInstall datasets library: pip install datasets")
            return None
        
        # Process each dataset
        all_processed = []
        for name, df in datasets.items():
            processed_df = self.process_dataset(df, name)
            if len(processed_df) > 0:
                all_processed.append(processed_df)
        
        if not all_processed:
            print("\n✗ No data processed")
            return None
        
        # Combine
        print("\n" + "="*60)
        print("COMBINING DATASETS")
        print("="*60)
        combined_df = pd.concat(all_processed, ignore_index=True)
        print(f"Combined: {len(combined_df)} samples")
        
        # Remove duplicates
        before = len(combined_df)
        combined_df = combined_df.drop_duplicates(subset=['text'])
        print(f"Removed {before - len(combined_df)} duplicates")
        
        # Balance
        combined_df = self.balance_dataset(combined_df, samples_per_category=1200)
        
        # Shuffle
        combined_df = combined_df.sample(frac=1, random_state=42).reset_index(drop=True)
        
        # Save
        output_path = os.path.join(self.processed_dir, 'combined_dataset.csv')
        combined_df.to_csv(output_path, index=False, encoding='utf-8')
        print(f"\n✓ Saved to: {output_path}")
        
        # Statistics
        self.print_statistics(combined_df)
        
        print("\n" + "="*60)
        print("SUCCESS! Dataset ready for training")
        print("="*60)
        print(f"\nNext: python ml/train.py")
        
        return combined_df


def main():
    downloader = RealDatasetDownloader()
    downloader.run()


if __name__ == "__main__":
    main()
