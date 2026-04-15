# 🚀 Complete Free Deployment Guide

Deploy SmartSupport AI for **100% FREE** using Render (Backend) + Vercel (Frontend).

**Model Link**: https://drive.google.com/file/d/1Igb0dGI6-HlyccZWe8F82c2XA5m7TyZG/view

---

## 📋 Prerequisites

- GitHub account (you already have this ✅)
- Google account (for Render/Vercel login)
- Your repository: https://github.com/satvik-sharma-05/SmartSupportAI

---

## Part 1: Deploy Backend to Render (10 minutes)

### Step 1: Create Render Account
1. Go to https://render.com
2. Click "Get Started for Free"
3. Sign up with GitHub (recommended)
4. Authorize Render to access your repositories

### Step 2: Create Web Service
1. Click "New +" button (top right)
2. Select "Web Service"
3. Connect your GitHub repository:
   - Click "Connect account" if needed
   - Find "SmartSupportAI" repository
   - Click "Connect"

### Step 3: Configure Service
Fill in these settings:

**Basic Settings:**
- **Name**: `smartsupport-api` (or any name you like)
- **Region**: Choose closest to you (e.g., Oregon, Frankfurt)
- **Branch**: `main`
- **Root Directory**: Leave empty
- **Runtime**: `Python 3`

**Build Settings:**
- **Build Command**: 
  ```bash
  pip install -r requirements.txt
  ```

**Start Command**:
```bash
pip install gdown && gdown --fuzzy https://drive.google.com/file/d/1Igb0dGI6-HlyccZWe8F82c2XA5m7TyZG/view -O models/smartsupport_model/model.pt && uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

**Instance Type:**
- Select "Free" (0.1 CPU, 512 MB RAM)

### Step 4: Add Environment Variables
Scroll down to "Environment Variables" section:

Click "Add Environment Variable" and add:
- **Key**: `SECRET_KEY`
- **Value**: `your-super-secret-random-key-12345` (change this!)

Optional (for MongoDB):
- **Key**: `MONGODB_URI`
- **Value**: Your MongoDB connection string (if you have one)

### Step 5: Deploy!
1. Click "Create Web Service" button at the bottom
2. Wait 5-10 minutes for deployment
3. Watch the logs - you'll see:
   - Installing dependencies
   - Downloading model (this takes a few minutes)
   - Starting server

### Step 6: Get Your Backend URL
Once deployed, you'll see:
- Status: "Live" (green)
- Your URL: `https://smartsupport-api.onrender.com` (or similar)

**Copy this URL!** You'll need it for the frontend.

### Step 7: Test Backend
Open in browser: `https://your-backend-url.onrender.com/health`

Should return:
```json
{"status": "healthy", "model_loaded": true}
```

✅ **Backend deployed!**

---

## Part 2: Deploy Frontend to Vercel (5 minutes)

### Step 1: Create Vercel Account
1. Go to https://vercel.com
2. Click "Sign Up"
3. Sign up with GitHub
4. Authorize Vercel

### Step 2: Import Project
1. Click "Add New..." → "Project"
2. Find "SmartSupportAI" repository
3. Click "Import"

### Step 3: Configure Project
**Framework Preset**: Vite (should auto-detect)

**Root Directory**: 
- Click "Edit"
- Enter: `frontend`
- Click "Continue"

**Build Settings** (should auto-fill):
- Build Command: `npm run build`
- Output Directory: `dist`
- Install Command: `npm install`

### Step 4: Add Environment Variable
Click "Environment Variables" section:

Add variable:
- **Name**: `VITE_API_URL`
- **Value**: `https://your-backend-url.onrender.com` (your Render URL from Part 1)
- Click "Add"

### Step 5: Deploy!
1. Click "Deploy" button
2. Wait 2-3 minutes
3. Watch the build logs

### Step 6: Get Your Frontend URL
Once deployed:
- Status: "Ready"
- Your URL: `https://smartsupport-ai.vercel.app` (or similar)

### Step 7: Test Frontend
1. Open your Vercel URL
2. You should see the homepage
3. Click "Get Started" or "Sign Up"
4. Create an account
5. Go to "Predict" page
6. Enter: "I was charged twice for my subscription"
7. Click "Predict"
8. Should see AI prediction! 🎉

✅ **Frontend deployed!**

---

## Part 3: Optional - Add MongoDB (5 minutes)

### Step 1: Create MongoDB Atlas Account
1. Go to https://www.mongodb.com/cloud/atlas
2. Sign up for free
3. Create organization and project

### Step 2: Create Free Cluster
1. Click "Build a Database"
2. Choose "M0 Free" tier
3. Select region (same as Render)
4. Cluster name: `SmartSupport`
5. Click "Create"

### Step 3: Create Database User
1. Security → Database Access
2. Click "Add New Database User"
3. Username: `smartsupport`
4. Password: Generate secure password (save it!)
5. Database User Privileges: "Read and write to any database"
6. Click "Add User"

### Step 4: Whitelist IP
1. Security → Network Access
2. Click "Add IP Address"
3. Click "Allow Access from Anywhere"
4. IP: `0.0.0.0/0`
5. Click "Confirm"

### Step 5: Get Connection String
1. Database → Connect
2. Choose "Connect your application"
3. Driver: Python, Version: 3.12 or later
4. Copy connection string:
   ```
   mongodb+srv://smartsupport:<password>@cluster.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```
5. Replace `<password>` with your actual password

### Step 6: Add to Render
1. Go back to Render dashboard
2. Click your service "smartsupport-api"
3. Go to "Environment" tab
4. Click "Add Environment Variable"
5. Key: `MONGODB_URI`
6. Value: Your connection string (with password filled in)
7. Click "Save Changes"
8. Service will auto-redeploy

✅ **Database connected!**

---

## 🎯 Final Testing

### Test Complete Flow:
1. Open your Vercel URL
2. Sign up for account
3. Login
4. Go to Dashboard (should show stats if MongoDB connected)
5. Go to Predict page
6. Test these tickets:

**Test 1 - Billing:**
```
I was charged twice for my subscription this month
```
Expected: Category = Billing, Priority = High

**Test 2 - Technical:**
```
The application crashes when I upload files
```
Expected: Category = Technical, Priority = High

**Test 3 - Account:**
```
How do I change my password?
```
Expected: Category = Account, Priority = Low/Medium

**Test 4 - General:**
```
What features are included in the pro plan?
```
Expected: Category = General, Priority = Low

---

## 📊 Your Deployed URLs

**Frontend**: `https://your-app.vercel.app`
**Backend**: `https://your-app.onrender.com`
**API Docs**: `https://your-app.onrender.com/docs`

---

## 🐛 Troubleshooting

### Backend Issues:

**"Application failed to respond"**
- Check Render logs for errors
- Verify model downloaded successfully
- Check if service is sleeping (free tier sleeps after 15 min)

**"Model not found"**
- Check start command includes model download
- Verify Google Drive link is correct
- Check logs for download errors

**Slow first request (30-60 seconds)**
- Normal on free tier - service is waking up
- Subsequent requests will be fast

### Frontend Issues:

**"Network Error" when predicting**
- Check VITE_API_URL is correct
- Verify backend is running
- Check browser console for CORS errors

**Can't connect to backend**
- Make sure backend URL doesn't have trailing slash
- Verify backend health endpoint works
- Check Vercel environment variables

### MongoDB Issues:

**"Database connection failed"**
- Verify connection string is correct
- Check password has no special characters (or URL encode them)
- Verify IP whitelist includes 0.0.0.0/0
- App still works without MongoDB (predictions only)

---

## 💡 Pro Tips

1. **Keep Backend Alive**: Use UptimeRobot (free) to ping your backend every 5 minutes
   - Sign up at https://uptimerobot.com
   - Add monitor: `https://your-backend.onrender.com/health`
   - Interval: 5 minutes

2. **Custom Domain**: Both Render and Vercel support custom domains for free
   - Vercel: Settings → Domains
   - Render: Settings → Custom Domain

3. **Monitor Logs**: 
   - Render: Click service → Logs tab
   - Vercel: Deployments → Click deployment → View Function Logs

4. **Auto-Deploy**: Both platforms auto-deploy when you push to GitHub
   ```bash
   git add .
   git commit -m "Update feature"
   git push
   ```

---

## 🎉 Success!

Your SmartSupport AI is now live and accessible worldwide!

**Share your app:**
- Frontend: Your Vercel URL
- API: Your Render URL
- GitHub: https://github.com/satvik-sharma-05/SmartSupportAI

**Free tier limits:**
- Render: 750 hours/month (enough for 24/7 with one app)
- Vercel: 100GB bandwidth/month
- MongoDB: 512MB storage

**Next steps:**
- Share on LinkedIn/Twitter
- Add to your portfolio
- Get feedback from users
- Iterate and improve!

Congratulations! 🚀🎊
