# 🚀 START HERE - Quick Deployment Guide

## Your Model Link
https://drive.google.com/file/d/1Igb0dGI6-HlyccZWe8F82c2XA5m7TyZG/view

## 3 Simple Steps to Deploy (15-20 minutes total)

### Step 1: Deploy Backend to Render (10 min)

1. Go to **https://render.com** and sign up with GitHub
2. Click **"New +"** → **"Web Service"**
3. Connect your **SmartSupportAI** repository
4. Fill in these settings:
   - **Name**: `smartsupport-api`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**:
     ```bash
     pip install gdown && gdown --fuzzy https://drive.google.com/file/d/1Igb0dGI6-HlyccZWe8F82c2XA5m7TyZG/view -O models/smartsupport_model/model.pt && uvicorn app.main:app --host 0.0.0.0 --port $PORT
     ```
   - **Instance Type**: Free
5. Add Environment Variable:
   - Key: `SECRET_KEY`
   - Value: `your-random-secret-key-change-this`
6. Click **"Create Web Service"**
7. Wait 5-10 minutes for deployment
8. **Copy your backend URL** (e.g., `https://smartsupport-api.onrender.com`)

### Step 2: Deploy Frontend to Vercel (5 min)

1. Go to **https://vercel.com** and sign up with GitHub
2. Click **"Add New..."** → **"Project"**
3. Import **SmartSupportAI** repository
4. Configure:
   - **Root Directory**: `frontend`
   - **Framework**: Vite (auto-detected)
5. Add Environment Variable:
   - Name: `VITE_API_URL`
   - Value: Your Render backend URL from Step 1
6. Click **"Deploy"**
7. Wait 2-3 minutes
8. Your app is LIVE! 🎉

### Step 3: Test Your App

1. Open your Vercel URL
2. Sign up for an account
3. Go to "Predict" page
4. Test with: "I was charged twice for my subscription"
5. See AI prediction! ✅

## 💰 Cost: $0 (100% FREE!)

- Render: 750 hours/month free
- Vercel: Unlimited deployments
- Total: FREE forever!

## 📚 Need More Details?

Read **DEPLOY_STEP_BY_STEP.md** for:
- Screenshots and detailed instructions
- MongoDB setup (optional)
- Troubleshooting tips
- Pro tips and monitoring

## 🐛 Quick Troubleshooting

**Backend not responding?**
- Wait 30-60 seconds (free tier wakes up slowly)
- Check Render logs for errors

**Frontend can't connect?**
- Verify VITE_API_URL is correct
- Make sure backend is running

**Model not loading?**
- Check Render logs for download errors
- Verify Google Drive link works

## ✅ You're Done!

Your SmartSupport AI is now deployed and accessible worldwide!

**Share your app:**
- Add to your portfolio
- Share on LinkedIn
- Show to potential employers
- Get user feedback

Congratulations! 🎊
