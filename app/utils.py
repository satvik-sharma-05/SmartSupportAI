import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download required NLTK data (run once)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

STOP_WORDS = set(stopwords.words('english'))


def preprocess_text(text: str) -> str:
    """
    Clean and preprocess ticket text.
    
    Steps:
    1. Lowercase conversion
    2. Remove punctuation
    3. Tokenization
    4. Remove stopwords
    5. Join tokens
    """
    if not text or not isinstance(text, str):
        return ""
    
    # Lowercase
    text = text.lower()
    
    # Remove punctuation and special characters
    text = re.sub(r'[^a-z0-9\s]', '', text)
    
    # Tokenize
    tokens = word_tokenize(text)
    
    # Remove stopwords
    tokens = [word for word in tokens if word not in STOP_WORDS and len(word) > 2]
    
    # Join back
    return ' '.join(tokens)


def calculate_priority(category: str, text: str, confidence: float) -> str:
    """
    Rule-based priority assignment with keyword detection.
    """
    text_lower = text.lower()
    
    # High priority keywords
    urgent_keywords = ['urgent', 'critical', 'emergency', 'asap', 'immediately', 
                       'down', 'not working', 'broken', 'cant access', 'locked out']
    
    # Check for urgent keywords
    has_urgent = any(keyword in text_lower for keyword in urgent_keywords)
    
    # Priority logic
    if has_urgent or confidence > 0.9:
        return "High"
    elif category in ["Technical", "Billing"] and confidence > 0.7:
        return "High"
    elif confidence > 0.6:
        return "Medium"
    else:
        return "Low"
