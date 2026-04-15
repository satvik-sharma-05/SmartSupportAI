# 🚀 Deployment Guide

## Current Deployment (Live)

✅ **Backend**: https://smartsupportai-backend.onrender.com
✅ **Frontend**: https://smart-support-ai-sandy.vercel.app/

This app is deployed on **100% FREE** tier using:
- **Render Free Tier** (Backend)
- **Vercel Free Tier** (Frontend)

---

## Deploy Your Own Instance

### Backend (Render)

1. **Create Render Account**
   - Go to https://render.com
   - Sign up with GitHub

2. **Create Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

3. **Configure Service**
   - **Name**: `smartsupportai-backend` (or your choice)
   - **Branch**: `main`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `bash start.sh`
   - **Instance Type**: Free

4. **Deploy**
   - Click "Create Web Service"
   - Wait 2-3 minutes for deployment
   - Your backend will be live at `https://your-app.onrender.com`

### Frontend (Vercel)

1. **Create Vercel Account**
   - Go to https://vercel.com
   - Sign up with GitHub

2. **Import Project**
   - Click "Add New..." → "Project"
   - Select your repository

3. **Configure Project**
   - **Framework**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

4. **Add Environment Variable**
   - **Name**: `VITE_API_URL`
   - **Value**: `https://your-backend.onrender.com` (from step 1)

5. **Deploy**
   - Click "Deploy"
   - Wait 2-3 minutes
   - Your frontend will be live at `https://your-app.vercel.app`

---

## Testing Your Deployment

### Test Backend
```bash
curl https://your-backend.onrender.com/health
```

Expected response:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "model": "rule-based-v1"
}
```

### Test Prediction
```bash
curl -X POST https://your-backend.onrender.com/predict \
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

## Architecture

### Current Setup (Free Tier)
- **Classification**: Rule-based keyword matching
- **RAM Usage**: < 200MB
- **Startup Time**: 5 seconds
- **Accuracy**: ~75-80%
- **Cost**: $0/month

### Why Rule-Based?
The free tier has 512MB RAM limit. A full ML model (PyTorch + transformers + 704MB model) exceeds this limit. The rule-based classifier provides good accuracy while staying within free tier limits.

---

## Upgrading to ML Model (Optional)

If you need higher accuracy (~90%), you can upgrade:

### Option 1: Paid Render Plan
- Upgrade to Standard plan ($21/month)
- Gives 2GB RAM
- Can run full PyTorch model

### Option 2: Hugging Face Spaces
- Deploy ML model to HF Spaces (Free with GPU!)
- Keep lightweight backend on Render
- Backend calls HF API for predictions

---

## Troubleshooting

### Backend Issues

**"Application failed to respond"**
- Check Render logs for errors
- Verify start command is correct
- Free tier sleeps after 15 min inactivity (first request will be slow)

**"Out of memory"**
- You're using the full ML model
- Switch to lightweight version (this repo)
- Or upgrade to paid plan

### Frontend Issues

**"Network Error"**
- Check `VITE_API_URL` environment variable
- Verify backend is running
- Check browser console for CORS errors

**Can't connect to backend**
- Make sure backend URL doesn't have trailing slash
- Verify backend health endpoint works
- Check Vercel environment variables

---

## Free Tier Limits

### Render Free Tier
- 512MB RAM
- 750 hours/month (enough for 24/7)
- Sleeps after 15 min inactivity
- 100GB bandwidth/month

### Vercel Free Tier
- 100GB bandwidth/month
- Unlimited deployments
- Automatic HTTPS
- Global CDN

---

## Next Steps

1. ✅ Deploy backend to Render
2. ✅ Deploy frontend to Vercel
3. ✅ Test the application
4. 🎉 Share your project!

---

**Need help?** Open an issue on GitHub!
