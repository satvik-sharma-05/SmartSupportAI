"""
Download and prepare real-world datasets from Kaggle
Uses kagglehub to download datasets automatically
"""
import os
import pandas as pd
import numpy as np
import re
from typing import List, Dict
import warnings
warnings.filterwarnings('ignore')

# Check if kagglehub is installed
try:
    import kagglehub
    KAGGLEHUB_AVAILABLE = True
except ImportError:
    KAGGLEHUB_AVAILABLE = False
    print("WARNING: kagglehub not installed. Install with: pip install kagglehub")


class KaggleDatasetDownloader:
    """Download and process Kaggle datasets for SmartSupport AI"""
    
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
            'severe', 'major', 'outage', 'dead', 'frozen'
        ]
        
        self.medium_priority_keywords = [
            'delay', 'slow', 'issue', 'problem', 'help', 'need',
            'question', 'how to', 'confused', 'unclear', 'intermittent',
            'sometimes', 'occasionally'
        ]
        
        # Category mapping
        self.category_mapping = {
            # Technical
            'technical': 'Technical', 'tech': 'Technical', 'software': 'Technical',
            'hardware': 'Technical', 'bug': 'Technical', 'error': 'Technical',
            'system': 'Technical', 'network': 'Technical', 'connectivity': 'Technical',
            'access': 'Technical', 'login': 'Technical', 'password': 'Technical',
            'it': 'Technical', 'computer': 'Technical', 'device': 'Technical',
            
            # Billing
            'billing': 'Billing', 'payment': 'Billing', 'invoice': 'Billing',
            'charge': 'Billing', 'refund': 'Billing', 'subscription': 'Billing',
            'pricing': 'Billing', 'cost': 'Billing', 'money': 'Billing',
            'credit card': 'Billing', 'bank': 'Billing',
            
            # Account
            'account': 'Account', 'profile': 'Account', 'settings': 'Account',
            'user': 'Account', 'registration': 'Account', 'signup': 'Account',
            'personal': 'Account', 'information': 'Account',
            
            # General
            'general': 'General', 'inquiry': 'General', 'question': 'General',
            'other': 'General', 'misc': 'General', 'miscellaneous': 'General',
        }
    
    def download_kaggle_datasets(self) -> Dict[str, pd.DataFrame]:
        """Download datasets from Kaggle using kagglehub"""
        if not KAGGLEHUB_AVAILABLE:
            print("ERROR: kagglehub not installed")
            print("Install with: pip install kagglehub")
            return {}
        
        datasets = {}
        
        # Dataset 1: Customer Support Ticket Dataset
        print("\n" + "="*60)
        print("Downloading Dataset 1: Customer Support Tickets")
        print("="*60)
        try:
            path = kagglehub.dataset_download("suraj520/customer-support-ticket-dataset")
            print(f"✓ Path to dataset files: {path}")
            
            # Find and load CSV files
            csv_files = [f for f in os.listdir(path) if f.endswith('.csv')]
            if csv_files:
                df1 = pd.read_csv(os.path.join(path, csv_files[0]))
                print(f"✓ Loaded {len(df1)} records from {csv_files[0]}")
                print(f"  Columns: {list(df1.columns)}")
                datasets['customer_support'] = df1
            else:
                print(f"✗ No CSV files found in {path}")
        except Exception as e:
            print(f"✗ Failed to download: {e}")
        
        # Dataset 2: IT Service Ticket Classification
        print("\n" + "="*60)
        print("Downloading Dataset 2: IT Service Tickets")
        print("="*60)
        try:
            path = kagglehub.dataset_download("adisongoh/it-service-ticket-classification-dataset")
            print(f"✓ Path to dataset files: {path}")
            
            # Find and load CSV files
            csv_files = [f for f in os.listdir(path) if f.endswith('.csv')]
            if csv_files:
                df2 = pd.read_csv(os.path.join(path, csv_files[0]))
                print(f"✓ Loaded {len(df2)} records from {csv_files[0]}")
                print(f"  Columns: {list(df2.columns)}")
                datasets['it_service'] = df2
            else:
                print(f"✗ No CSV files found in {path}")
        except Exception as e:
            print(f"✗ Failed to download: {e}")
        
        # Dataset 3: Consumer Complaint Dataset
        print("\n" + "="*60)
        print("Downloading Dataset 3: Consumer Complaints")
        print("="*60)
        try:
            path = kagglehub.dataset_download("namigabbasov/consumer-complaint-dataset")
            print(f"✓ Path to dataset files: {path}")
            
            # Find and load CSV files
            csv_files = [f for f in os.listdir(path) if f.endswith('.csv')]
            if csv_files:
                df3 = pd.read_csv(os.path.join(path, csv_files[0]))
                print(f"✓ Loaded {len(df3)} records from {csv_files[0]}")
                print(f"  Columns: {list(df3.columns)}")
                
                # Sample if too large
                if len(df3) > 10000:
                    print(f"  Dataset too large, sampling 10000 records...")
                    df3 = df3.sample(n=10000, random_state=42)
                
                datasets['consumer_complaints'] = df3
            else:
                print(f"✗ No CSV files found in {path}")
        except Exception as e:
            print(f"✗ Failed to download: {e}")
        
        return datasets
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        if not isinstance(text, str) or pd.isna(text):
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^a-zA-Z0-9\s.,!?-]', '', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text.strip()
    
    def normalize_category(self, category: str, text: str = "") -> str:
        """Normalize category labels with intelligent mapping"""
        if not isinstance(category, str) or pd.isna(category):
            # Try to infer from text
            if text:
                text_lower = text.lower()
                if any(word in text_lower for word in ['payment', 'billing', 'charge', 'invoice']):
                    return 'Billing'
                elif any(word in text_lower for word in ['error', 'bug', 'crash', 'technical']):
                    return 'Technical'
                elif any(word in text_lower for word in ['account', 'profile', 'login']):
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
        
        # Keyword-based inference
        if any(word in category_lower for word in ['tech', 'software', 'hardware', 'system']):
            return 'Technical'
        elif any(word in category_lower for word in ['bill', 'pay', 'money', 'charge']):
            return 'Billing'
        elif any(word in category_lower for word in ['account', 'user', 'profile']):
            return 'Account'
        
        return 'General'
    
    def assign_priority(self, text: str) -> str:
        """Assign priority based on keywords and urgency indicators"""
        if not isinstance(text, str) or pd.isna(text):
            return 'Low'
        
        text_lower = text.lower()
        
        # Count high priority keywords
        high_count = sum(1 for keyword in self.high_priority_keywords if keyword in text_lower)
        
        # Strong high priority indicators
        if high_count >= 2:
            return 'High'
        
        if any(word in text_lower for word in ['urgent', 'critical', 'emergency', 'asap', 'immediately']):
            return 'High'
        
        # Count medium priority keywords
        medium_count = sum(1 for keyword in self.medium_priority_keywords if keyword in text_lower)
        
        if medium_count >= 2 or high_count == 1:
            return 'Medium'
        
        # Check for question marks (usually lower priority)
        if '?' in text and high_count == 0:
            return 'Low'
        
        return 'Low'
    
    def process_dataset(self, df: pd.DataFrame, dataset_name: str) -> pd.DataFrame:
        """Process individual dataset"""
        print(f"\nProcessing {dataset_name}...")
        print(f"  Original shape: {df.shape}")
        print(f"  Columns: {list(df.columns)}")
        
        processed_data = []
        
        # Identify text and category columns with better matching
        text_col = None
        category_col = None
        
        # Try to find text column
        text_candidates = ['text', 'description', 'ticket', 'complaint', 'issue', 
                          'message', 'content', 'summary', 'title', 'document', 'narrative']
        for col in df.columns:
            col_lower = col.lower().strip()
            if any(candidate in col_lower for candidate in text_candidates):
                text_col = col
                break
        
        # Try to find category column
        category_candidates = ['category', 'type', 'label', 'class', 'classification', 
                              'product', 'issue', 'topic', 'group']
        for col in df.columns:
            col_lower = col.lower().strip()
            if any(candidate in col_lower for candidate in category_candidates):
                category_col = col
                break
        
        if text_col is None:
            print(f"  ✗ Could not identify text column")
            print(f"  Available columns: {list(df.columns)}")
            return pd.DataFrame()
        
        print(f"  Text column: {text_col}")
        print(f"  Category column: {category_col if category_col else 'None (will infer)'}")
        
        # Process rows
        for idx, row in df.iterrows():
            text = str(row[text_col]) if text_col else ""
            text_clean = self.clean_text(text)
            
            # Skip if text too short
            if len(text_clean) < 10:
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
        print(f"  ✓ Processed {len(result_df)} valid samples")
        
        return result_df
    
    def identify_column(self, df: pd.DataFrame, possible_names: List[str]) -> str:
        """Identify column by matching possible names"""
        for col in df.columns:
            col_lower = col.lower().strip()
            for name in possible_names:
                if name.lower() in col_lower or col_lower in name.lower():
                    return col
        return None
    
    def balance_dataset(self, df: pd.DataFrame, samples_per_category: int = 1000) -> pd.DataFrame:
        """Balance dataset by category"""
        print("\nBalancing dataset...")
        print(f"  Target: {samples_per_category} samples per category")
        
        balanced_dfs = []
        
        for category in df['category'].unique():
            category_df = df[df['category'] == category]
            
            if len(category_df) > samples_per_category:
                # Downsample
                category_df = category_df.sample(n=samples_per_category, random_state=42)
            elif len(category_df) < samples_per_category:
                # Upsample if significantly underrepresented
                if len(category_df) < samples_per_category // 2:
                    print(f"  Warning: {category} has only {len(category_df)} samples")
            
            balanced_dfs.append(category_df)
        
        balanced_df = pd.concat(balanced_dfs, ignore_index=True)
        print(f"  Balanced to {len(balanced_df)} total samples")
        
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
        print(f"  Mean: {df['text_length'].mean():.0f} characters")
        print(f"  Median: {df['text_length'].median():.0f} characters")
        print(f"  Min: {df['text_length'].min():.0f} characters")
        print(f"  Max: {df['text_length'].max():.0f} characters")
        
        print("\nSample records:")
        for idx, row in df.sample(n=min(3, len(df))).iterrows():
            print(f"\n  Category: {row['category']} | Priority: {row['priority']}")
            print(f"  Text: {row['text'][:100]}...")
    
    def run(self):
        """Main execution flow"""
        print("\n" + "="*60)
        print("KAGGLE DATASET DOWNLOADER & PROCESSOR")
        print("SmartSupport AI - Real-World Dataset Integration")
        print("="*60)
        
        # Download datasets
        datasets = self.download_kaggle_datasets()
        
        if not datasets:
            print("\n✗ No datasets downloaded. Check your Kaggle authentication.")
            print("\nSetup Kaggle API:")
            print("1. Go to https://www.kaggle.com/settings")
            print("2. Create new API token")
            print("3. Place kaggle.json in ~/.kaggle/")
            return None
        
        # Process each dataset
        all_processed = []
        for name, df in datasets.items():
            processed_df = self.process_dataset(df, name)
            if len(processed_df) > 0:
                all_processed.append(processed_df)
        
        if not all_processed:
            print("\n✗ No data processed successfully")
            return None
        
        # Combine all datasets
        print("\n" + "="*60)
        print("COMBINING DATASETS")
        print("="*60)
        combined_df = pd.concat(all_processed, ignore_index=True)
        print(f"Combined {len(combined_df)} total samples")
        
        # Remove duplicates
        print("\nRemoving duplicates...")
        before = len(combined_df)
        combined_df = combined_df.drop_duplicates(subset=['text'])
        print(f"  Removed {before - len(combined_df)} duplicates")
        
        # Balance dataset
        combined_df = self.balance_dataset(combined_df, samples_per_category=1000)
        
        # Shuffle
        combined_df = combined_df.sample(frac=1, random_state=42).reset_index(drop=True)
        
        # Save
        output_path = os.path.join(self.processed_dir, 'combined_dataset.csv')
        combined_df.to_csv(output_path, index=False, encoding='utf-8')
        print(f"\n✓ Saved to: {output_path}")
        
        # Print statistics
        self.print_statistics(combined_df)
        
        print("\n" + "="*60)
        print("DATASET PREPARATION COMPLETE!")
        print("="*60)
        print(f"\nNext step: Train the model")
        print(f"  Command: python ml/train.py")
        
        return combined_df


def main():
    downloader = KaggleDatasetDownloader()
    downloader.run()


if __name__ == "__main__":
    main()
