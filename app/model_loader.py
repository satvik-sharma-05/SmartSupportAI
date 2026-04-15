"""
Model loading utilities for inference
"""
import torch
from transformers import AutoTokenizer
import os

from ml.config import Config
from ml.model import MultiTaskTicketClassifier


class ModelLoader:
    """Singleton class for loading and caching the model"""
    
    _instance = None
    _model = None
    _tokenizer = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelLoader, cls).__new__(cls)
        return cls._instance
    
    def load_model(self):
        """Load model and tokenizer (supports both local and Colab-trained models)"""
        if self._model is None or self._tokenizer is None:
            print("Loading model and tokenizer...")
            
            # Set device (do this here, not at import time)
            import torch
            Config.DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            print(f"  Device: {Config.DEVICE}")
            
            # Check if model exists
            model_path = f"{Config.MODEL_SAVE_PATH}/model.pt"
            if not os.path.exists(model_path):
                raise FileNotFoundError(
                    f"Model not found at {model_path}. "
                    "Please train the model first:\n"
                    "  Option 1 (Local): python ml/train.py\n"
                    "  Option 2 (Colab): Upload train_colab.py to Google Colab\n"
                    "  Then run: python integrate_colab_model.py"
                )
            
            # Load checkpoint
            checkpoint = torch.load(model_path, map_location=Config.DEVICE)
            
            # Check if it's a Colab-trained model (has metadata)
            if isinstance(checkpoint, dict) and 'model_state_dict' in checkpoint:
                print("✓ Detected Colab-trained model")
                model_name = checkpoint.get('model_name', Config.MODEL_NAME)
                num_categories = len(checkpoint.get('category_to_id', {}))
                num_priorities = len(checkpoint.get('priority_to_id', {}))
                
                # Load tokenizer
                self._tokenizer = AutoTokenizer.from_pretrained(model_name)
                
                # Load model with correct dimensions
                self._model = MultiTaskTicketClassifier(
                    model_name,
                    num_categories if num_categories > 0 else 4,
                    num_priorities if num_priorities > 0 else 3
                )
                self._model.load_state_dict(checkpoint['model_state_dict'])
                
                print(f"  Model: {model_name}")
                print(f"  Categories: {num_categories}")
                print(f"  Priorities: {num_priorities}")
            else:
                # Legacy model format
                print("✓ Detected local-trained model")
                self._tokenizer = AutoTokenizer.from_pretrained(Config.TOKENIZER_SAVE_PATH)
                self._model = MultiTaskTicketClassifier(Config.MODEL_NAME)
                self._model.load_state_dict(checkpoint)
            
            self._model.to(Config.DEVICE)
            self._model.eval()
            
            print(f"✓ Model loaded from {model_path}")
        
        return self._model, self._tokenizer
    
    def get_model(self):
        """Get loaded model"""
        if self._model is None:
            self.load_model()
        return self._model
    
    def get_tokenizer(self):
        """Get loaded tokenizer"""
        if self._tokenizer is None:
            self.load_model()
        return self._tokenizer


# Global instance
model_loader = ModelLoader()
