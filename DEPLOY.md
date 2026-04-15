# Quick Deployment Guide

## 🚀 Deploy to Render (Free - Recommended)

### Backend

1. Go to [render.com](https://render.com) and sign up
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: smartsupport-api
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: Free
5. Add Environment Variable:
   - `SECRET_KEY` = `your-random-secret-key`
6. Click "Create Web Service"
7. Wait 5-10 minutes for deployment
8. Copy your backend URL (e.g., `https://smartsupport-api.onrender.com`)

### Frontend

1. Go to [vercel.com](https://vercel.com) and sign up
2. Click "New Project"
3. Import your GitHub repository
4. Configure:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
5. Add Environment Variable:
   - `VITE_API_URL` = `https://smartsupport-api.onrender.com` (your backend URL)
6. Click "Deploy"
7. Wait 2-3 minutes
8. Your app is live!

## ⚡ Alternative: Deploy to Railway

### Backend + Frontend Together

1. Go to [railway.app](https://railway.app)
2. Click "Start a New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository
5. Railway auto-detects and deploys both backend and frontend
6. Add environment variables in the dashboard
7. Done!

## 🗄️ Optional: Add MongoDB

### MongoDB Atlas (Free 512MB)

1. Go to [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
2. Create free account
3. Create free cluster (M0)
4. Create database user
5. Whitelist IP: `0.0.0.0/0` (allow all)
6. Get connection string
7. Add to your backend environment variables:
   - `MONGODB_URI` = `mongodb+srv://username:password@cluster.mongodb.net/smartsupport`

## 🔍 Troubleshooting

**Backend won't start:**
- Check logs in Render dashboard
- Verify requirements.txt is correct
- Ensure model file exists in `models/` directory

**Frontend can't connect to backend:**
- Check VITE_API_URL is set correctly
- Verify backend is running
- Check CORS settings in backend

**Model file too large:**
- Use Git LFS for large files
- Or upload model separately to cloud storage
- Update model_loader.py to download from URL

## 📊 Free Tier Limits

**Render:**
- 750 hours/month free
- Sleeps after 15 min inactivity
- 512MB RAM

**Vercel:**
- 100GB bandwidth/month
- Unlimited deployments
- Automatic HTTPS

**Railway:**
- $5 free credit/month
- ~500 hours runtime
- 1GB RAM

## 💡 Tips

1. **Backend sleeps on free tier**: First request takes 30-60s to wake up
2. **Keep backend alive**: Use a service like UptimeRobot to ping every 5 minutes
3. **Optimize model**: Consider using a smaller model for faster cold starts
4. **Use CDN**: Deploy frontend to Vercel/Netlify for better performance

## 🎯 Production Checklist

- [ ] Change SECRET_KEY to random string
- [ ] Set up MongoDB for ticket storage
- [ ] Configure CORS for your frontend domain
- [ ] Add error monitoring (Sentry)
- [ ] Set up analytics
- [ ] Add rate limiting
- [ ] Enable HTTPS (automatic on Render/Vercel)
- [ ] Test all API endpoints
- [ ] Monitor performance

Your app is now live and free! 🎉
