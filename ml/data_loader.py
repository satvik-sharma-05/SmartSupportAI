"""
Advanced data loader for SmartSupport AI - Real Datasets Only
"""
import pandas as pd
import os
import sys


class DatasetLoader:
    """Load and process real support ticket datasets from Kaggle"""
    
    def __init__(self):
        self.unified_df = None
        self.processed_path = 'data/processed/combined_dataset.csv'
    
    def load_real_dataset(self) -> pd.DataFrame:
        """Load real dataset from processed directory"""
        print("Loading real-world dataset...")
        
        if not os.path.exists(self.processed_path):
            print("\n" + "="*60)
            print("ERROR: REAL DATASET NOT FOUND")
            print("="*60)
            print(f"\nExpected file: {self.processed_path}")
            print("\nThis project uses ONLY real-world datasets from Kaggle.")
            print("\nTo download real datasets, run:")
            print("  python ml/download_datasets.py")
            print("\nOr:")
            print("  python ml/setup_real_datasets.py")
            print("\nDatasets will be downloaded from:")
            print("  - suraj520/customer-support-ticket-dataset")
            print("  - adisongoh/it-service-ticket-classification-dataset")
            print("  - namigabbasov/consumer-complaint-dataset")
            print("\n" + "="*60)
            sys.exit(1)
        
        df = pd.read_csv(self.processed_path)
        print(f"✓ Loaded {len(df)} real-world samples from {self.processed_path}")
        
        # Validate required columns
        required_cols = ['text', 'category', 'priority']
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            print(f"\n✗ ERROR: Missing required columns: {missing_cols}")
            print("Please re-run: python ml/download_datasets.py")
            sys.exit(1)
        
        return df
    
    def process_dataset(self) -> pd.DataFrame:
        """Main method to process dataset"""
        print("\n" + "="*60)
        print("LOADING REAL-WORLD DATASET")
        print("="*60)
        
        df = self.load_real_dataset()
        self.unified_df = df
        
        print("\n" + "="*60)
        print("DATASET SUMMARY")
        print("="*60)
        print(f"Total samples: {len(df)}")
        print(f"\nCategory distribution:")
        print(df['category'].value_counts())
        print(f"\nPriority distribution:")
        print(df['priority'].value_counts())
        
        if 'source' in df.columns:
            print(f"\nSource distribution:")
            print(df['source'].value_counts())
        
        print("="*60)
        
        return df
    
    def save_processed_dataset(self, df: pd.DataFrame, filepath: str = 'data/unified_dataset.csv'):
        """Save processed dataset"""
        self.unified_df = df
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        self.unified_df.to_csv(filepath, index=False)
        print(f"✓ Dataset saved to {filepath}")


if __name__ == "__main__":
    loader = DatasetLoader()
    df = loader.process_dataset()
    loader.save_processed_dataset(df)
    print("\n✓ Data loading complete!")
