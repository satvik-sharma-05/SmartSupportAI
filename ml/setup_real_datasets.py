"""
Setup Real Datasets for SmartSupport AI
Downloads only real-world datasets from Kaggle - NO SYNTHETIC DATA
"""
import os
import sys

def check_kagglehub():
    """Check if kagglehub is installed"""
    try:
        import kagglehub
        print("✓ kagglehub is installed")
        return True
    except ImportError:
        print("✗ kagglehub is NOT installed")
        print("\nInstall with:")
        print("  pip install kagglehub")
        return False

def main():
    print("\n" + "="*60)
    print("SMARTSUPPORT AI - REAL DATASET SETUP")
    print("="*60)
    print("\nThis script will download ONLY real-world datasets from Kaggle")
    print("NO synthetic or sample data will be used")
    
    # Check kagglehub
    if not check_kagglehub():
        sys.exit(1)
    
    print("\n" + "="*60)
    print("DATASETS TO BE DOWNLOADED")
    print("="*60)
    print("\n1. Customer Support Ticket Dataset")
    print("   Source: suraj520/customer-support-ticket-dataset")
    print("   Description: Real customer support tickets")
    
    print("\n2. IT Service Ticket Classification Dataset")
    print("   Source: adisongoh/it-service-ticket-classification-dataset")
    print("   Description: Real IT service desk tickets")
    
    print("\n3. Consumer Complaint Dataset")
    print("   Source: namigabbasov/consumer-complaint-dataset")
    print("   Description: Real consumer complaints")
    
    print("\n" + "="*60)
    print("STARTING DOWNLOAD")
    print("="*60)
    
    # Import and run the downloader
    from download_datasets import KaggleDatasetDownloader
    
    downloader = KaggleDatasetDownloader()
    result = downloader.run()
    
    if result is not None:
        print("\n" + "="*60)
        print("SUCCESS!")
        print("="*60)
        print("\nReal datasets downloaded and processed successfully")
        print("Location: data/processed/combined_dataset.csv")
        print("\nNext step: Train the model")
        print("  python ml/train.py")
    else:
        print("\n" + "="*60)
        print("FAILED")
        print("="*60)
        print("\nCould not download datasets")
        print("\nTroubleshooting:")
        print("1. Ensure kagglehub is installed: pip install kagglehub")
        print("2. Check your internet connection")
        print("3. Kaggle API authentication may be required for some datasets")
        sys.exit(1)

if __name__ == "__main__":
    main()
