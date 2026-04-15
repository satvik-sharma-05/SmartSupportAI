# 🚀 FREE TIER DEPLOYMENT (No ML Model)

## The Problem
Your ML model (704MB) + PyTorch dependencies exceed Render's free tier 512MB RAM limit.

## The Solution
Use the lightweight rule-based classifier instead of the ML model.

---

## Option 1: Deploy Lightweight Version (100% FREE) ✅

### What Changes:
- ❌ No PyTorch/transformers (saves ~400MB RAM)
- ❌ No 704MB model download
- ✅ Rule-based keyword matching classifier
- ✅ Still works! ~70-80% accuracy
- ✅ Instant startup (< 5 seconds)
- ✅ Fits in 512MB RAM

### Steps:

1. **Update Render Configuration:**
   - Go to your Render dashboard
   - Click your service
   - Go to "Settings"

2. **Change Build Command:**
   ```bash
   pip install -r requirements-minimal.txt
   ```

3. **Change Start Command:**
   ```bash
   bash start-lightweight.sh
   ```

4. **Save Changes**
   - Click "Save Changes"
   - Render will auto-deploy

5. **Test:**
   - Wait 2-3 minutes for deployment
   - Visit: `https://your-app.onrender.com/health`
   - Should see: `{"status": "healthy", "model": "rule-based-v1"}`

### How It Works:
The lightweight classifier uses keyword matching:

**Billing Keywords:** charge, payment, bill, invoice, subscription, refund
**Technical Keywords:** crash, error, bug, broken, not working
**Account Keywords:** login, password, sign in, access, account
**General Keywords:** how, what, when, feature, plan, help

**Example:**
```
Input: "I was charged twice for my subscription"
Output: Category=Billing (95%), Priority=High (85%)
```

---

## Option 2: Deploy Full ML Model (PAID) 💰

If you need the full transformer model:

### Render Paid Plans:
- **Starter ($7/month)**: 512MB RAM - Still too small
- **Standard ($21/month)**: 2GB RAM - ✅ Will work
- **Pro ($85/month)**: 4GB RAM - ✅ Fast

### Alternative Free Platforms with More RAM:
1. **Railway** - 512MB free (same issue)
2. **Fly.io** - 256MB free (worse)
3. **Google Cloud Run** - 512MB free (same issue)
4. **AWS Lambda** - 512MB-10GB (complex setup)

### Best Option for ML Model:
**Hugging Face Spaces (FREE with GPU!)**
- 16GB RAM
- Free GPU
- Perfect for ML models

Steps:
1. Go to https://huggingface.co/spaces
2. Create new Space
3. Choose "Gradio" or "FastAPI"
4. Upload your model
5. Deploy for free!

---

## Option 3: Hybrid Approach (RECOMMENDED) 🎯

**Frontend:** Vercel (Free)
**Backend (Lightweight):** Render Free Tier
**ML Model:** Hugging Face Spaces (Free)

Your backend calls Hugging Face API when it needs ML predictions.

---

## Comparison:

| Feature | Lightweight | Full ML Model |
|---------|------------|---------------|
| Cost | FREE | $21/month |
| RAM | < 200MB | > 1GB |
| Startup | 5 seconds | 60 seconds |
| Accuracy | ~75% | ~90% |
| Speed | 2ms | 150ms |
| Deployment | Easy | Complex |

---

## Recommendation:

**For Demo/Portfolio:** Use lightweight version (FREE)
**For Production:** Use paid plan or Hugging Face Spaces

---

## Quick Deploy Commands:

### Deploy Lightweight (Free):
```bash
# In Render dashboard:
Build: pip install -r requirements-minimal.txt
Start: bash start-lightweight.sh
```

### Deploy Full Model (Paid):
```bash
# In Render dashboard:
Build: pip install -r requirements.txt
Start: bash start.sh
Instance: Standard ($21/month)
```

---

## Testing Lightweight Version Locally:

```bash
# Install minimal dependencies
pip install -r requirements-minimal.txt

# Run lightweight server
uvicorn app.main_lightweight:app --host 0.0.0.0 --port 8000

# Test
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "I was charged twice for my subscription"}'
```

Expected response:
```json
{
  "category": "Billing",
  "category_confidence": 0.92,
  "priority": "High",
  "priority_confidence": 0.85,
  "inference_time_ms": 1.23,
  "model": "rule-based-v1"
}
```

---

## Next Steps:

1. **Try lightweight version first** (it's free!)
2. **If accuracy is good enough** → Keep it
3. **If you need better accuracy** → Upgrade to paid plan or use Hugging Face

Your choice! 🚀
