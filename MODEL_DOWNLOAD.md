# Model Download Instructions

## ⚠️ Important: Model File Too Large for Git

The trained model (`models/smartsupport_model/model.pt`) is **703MB**, which exceeds GitHub's 100MB file size limit.

## 📥 Download the Model

### Option 1: Google Drive (Recommended)

1. Download the model from: [Google Drive Link - Add your link here]
2. Place it in: `models/smartsupport_model/model.pt`

### Option 2: Hugging Face Hub

Upload your model to Hugging Face and download it:

```python
# In app/model_loader.py, add download logic:
from huggingface_hub import hf_hub_download

model_path = hf_hub_download(
    repo_id="your-username/smartsupport-model",
    filename="model.pt",
    cache_dir="models/smartsupport_model"
)
```

### Option 3: Use Git LFS

```bash
# Install Git LFS
git lfs install

# Track large files
git lfs track "*.pt"
git lfs track "models/**/*.pt"

# Add and commit
git add .gitattributes
git add models/smartsupport_model/model.pt
git commit -m "Add model with Git LFS"
git push
```

## 🚀 For Deployment

### Render/Railway Deployment

Add this to your deployment script:

```bash
# In your start script or Procfile
#!/bin/bash

# Download model if not exists
if [ ! -f "models/smartsupport_model/model.pt" ]; then
    echo "Downloading model..."
    wget -O models/smartsupport_model/model.pt "YOUR_MODEL_DOWNLOAD_URL"
fi

# Start the app
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Environment Variable Approach

Store model URL in environment variable:

```python
# app/model_loader.py
import os
import requests

MODEL_URL = os.getenv("MODEL_DOWNLOAD_URL")

if not os.path.exists("models/smartsupport_model/model.pt"):
    print("Downloading model...")
    response = requests.get(MODEL_URL)
    with open("models/smartsupport_model/model.pt", "wb") as f:
        f.write(response.content)
```

## 📤 Upload Your Model

### To Google Drive:
1. Upload `models/smartsupport_model/model.pt` to Google Drive
2. Right-click → Share → Get link
3. Make sure link is set to "Anyone with the link can view"
4. Use the direct download link format:
   ```
   https://drive.google.com/uc?export=download&id=FILE_ID
   ```

### To Hugging Face:
```bash
pip install huggingface_hub

# Login
huggingface-cli login

# Upload
huggingface-cli upload your-username/smartsupport-model models/smartsupport_model/model.pt
```

## 🔧 Alternative: Use Smaller Model

If deployment is difficult, consider using a smaller model:

```python
# In ml/config.py, change to:
MODEL_NAME = "microsoft/deberta-v3-small"  # ~140MB instead of 703MB
```

Then retrain on Google Colab with the smaller model.

## ✅ Verification

After downloading the model, verify it works:

```bash
python -c "import torch; model = torch.load('models/smartsupport_model/model.pt', map_location='cpu'); print('Model loaded successfully!')"
```

## 📝 Current Setup

The model file is currently:
- **Location**: `models/smartsupport_model/model.pt`
- **Size**: 703.61 MB
- **Architecture**: microsoft/deberta-v3-base
- **Accuracy**: 73.33% category, 66.17% priority

For production deployment, choose one of the options above to handle the large model file.
