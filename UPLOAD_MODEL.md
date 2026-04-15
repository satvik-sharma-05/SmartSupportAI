# 📤 Upload Model to Cloud Storage

Your code is now on GitHub! But the model file (703MB) was excluded because it's too large.

## ⚡ Quick Solution: Upload to Google Drive

### Step 1: Upload Model
1. Go to [Google Drive](https://drive.google.com)
2. Upload `models/smartsupport_model/model.pt` (703MB)
3. Right-click the file → Share → Get link
4. Set to "Anyone with the link can view"
5. Copy the file ID from the URL:
   ```
   https://drive.google.com/file/d/FILE_ID_HERE/view
   ```

### Step 2: Update README
Add the download link to your README.md:
```markdown
## Model Download
Download the trained model (703MB):
[Download from Google Drive](https://drive.google.com/uc?export=download&id=YOUR_FILE_ID)

Place it in: `models/smartsupport_model/model.pt`
```

### Step 3: For Deployment
Add this to your deployment start script:

```bash
#!/bin/bash
# download_model.sh

MODEL_URL="https://drive.google.com/uc?export=download&id=YOUR_FILE_ID"
MODEL_PATH="models/smartsupport_model/model.pt"

if [ ! -f "$MODEL_PATH" ]; then
    echo "Downloading model..."
    mkdir -p models/smartsupport_model
    wget --no-check-certificate "$MODEL_URL" -O "$MODEL_PATH"
    echo "Model downloaded!"
fi
```

## 🤗 Alternative: Hugging Face Hub (Recommended for ML)

### Upload to Hugging Face
```bash
# Install Hugging Face CLI
pip install huggingface_hub

# Login
huggingface-cli login

# Upload model
huggingface-cli upload satvik-sharma-05/smartsupport-model models/smartsupport_model/model.pt model.pt
```

### Download in Code
Update `app/model_loader.py`:
```python
from huggingface_hub import hf_hub_download
import os

MODEL_PATH = "models/smartsupport_model/model.pt"

# Download if not exists
if not os.path.exists(MODEL_PATH):
    print("Downloading model from Hugging Face...")
    hf_hub_download(
        repo_id="satvik-sharma-05/smartsupport-model",
        filename="model.pt",
        local_dir="models/smartsupport_model",
        local_dir_use_symlinks=False
    )
```

## 🚀 For Render Deployment

Add environment variable in Render dashboard:
```
MODEL_DOWNLOAD_URL=https://drive.google.com/uc?export=download&id=YOUR_FILE_ID
```

Update your start command in Procfile:
```
web: bash download_model.sh && uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

## ✅ Verification

After uploading, test the download:
```bash
# Test Google Drive link
wget --no-check-certificate "YOUR_GOOGLE_DRIVE_URL" -O test_model.pt

# Check file size
ls -lh test_model.pt
# Should show ~704MB
```

## 📝 Update Your Repository

1. Upload model to Google Drive or Hugging Face
2. Get the download URL
3. Update README.md with download instructions
4. Commit and push:
   ```bash
   git add README.md
   git commit -m "Add model download instructions"
   git push
   ```

Your project is now complete and deployable! 🎉
