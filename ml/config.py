"""
Configuration for SmartSupport AI transformer model training
Enhanced for production-grade performance
"""

class Config:
    # Model Configuration
    MODEL_NAME = "microsoft/deberta-v3-base"  # Best performing model
    # Alternative models (uncomment to use):
    # MODEL_NAME = "roberta-base"  # Faster alternative
    # MODEL_NAME = "microsoft/deberta-v3-small"  # Smaller, faster
    
    MAX_LENGTH = 256
    
    # Training Configuration (Optimized)
    BATCH_SIZE = 16  # Adjust based on GPU memory
    LEARNING_RATE = 2e-5  # Optimal for transformers
    NUM_EPOCHS = 5  # Increased for better convergence
    WARMUP_STEPS = 500
    WEIGHT_DECAY = 0.01
    GRADIENT_ACCUMULATION_STEPS = 2  # Effective batch size = 32
    
    # Categories and Priority (Order MUST match trained model metadata)
    CATEGORIES = ["General", "Account", "Billing", "Technical"]
    PRIORITIES = ["Low", "Medium", "High"]
    NUM_CATEGORIES = len(CATEGORIES)
    NUM_PRIORITIES = len(PRIORITIES)
    
    # Paths
    MODEL_SAVE_PATH = "models/smartsupport_model"
    TOKENIZER_SAVE_PATH = "models/smartsupport_tokenizer"
    BEST_MODEL_PATH = "models/best_model.pt"
    
    # Device (set to CPU by default for faster startup, will use GPU if available when model loads)
    DEVICE = "cpu"  # Will be updated to actual device when model loads
    
    # Training Split
    TRAIN_SPLIT = 0.7
    VAL_SPLIT = 0.15
    TEST_SPLIT = 0.15
    
    # Multi-task Learning Weights
    CATEGORY_WEIGHT = 1.0
    PRIORITY_WEIGHT = 1.0
    
    # Inference
    CONFIDENCE_THRESHOLD = 0.5
    
    # Early Stopping
    EARLY_STOPPING_PATIENCE = 3
    
    # Data Augmentation
    USE_DATA_AUGMENTATION = False  # Set to True for more data
    
    @classmethod
    def get_category_id(cls, category: str) -> int:
        """Convert category name to ID"""
        return cls.CATEGORIES.index(category)
    
    @classmethod
    def get_priority_id(cls, priority: str) -> int:
        """Convert priority name to ID"""
        return cls.PRIORITIES.index(priority)
    
    @classmethod
    def get_category_name(cls, category_id: int) -> str:
        """Convert category ID to name"""
        return cls.CATEGORIES[category_id]
    
    @classmethod
    def get_priority_name(cls, priority_id: int) -> str:
        """Convert priority ID to name"""
        return cls.PRIORITIES[priority_id]
    
    @classmethod
    def print_config(cls):
        """Print configuration"""
        print("\n" + "="*60)
        print("MODEL CONFIGURATION")
        print("="*60)
        print(f"Model: {cls.MODEL_NAME}")
        print(f"Device: {cls.DEVICE}")
        print(f"Max Length: {cls.MAX_LENGTH}")
        print(f"Batch Size: {cls.BATCH_SIZE}")
        print(f"Learning Rate: {cls.LEARNING_RATE}")
        print(f"Epochs: {cls.NUM_EPOCHS}")
        print(f"Categories: {cls.CATEGORIES}")
        print(f"Priorities: {cls.PRIORITIES}")
        print("="*60)
