# ⚡ Quick Start Guide

## 🎯 Goal
Get SmartSupport AI running locally in 5 minutes.

## 📋 Prerequisites
- Python 3.8+
- Node.js 16+
- Git

## 🚀 Steps

### 1. Clone & Setup Backend (2 min)
```bash
git clone <your-repo>
cd SmartSupportAI
pip install -r requirements.txt
cp .env.example .env
```

### 2. Download Model (1 min)
⚠️ **Important**: Model file is 703MB, not in git repo.

Download from: [Add your link]
Place in: `models/smartsupport_model/model.pt`

### 3. Start Backend (30 sec)
```bash
uvicorn app.main:app --reload
```
✅ Backend running at: http://localhost:8000

### 4. Setup Frontend (1 min)
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```
✅ Frontend running at: http://localhost:3000

### 5. Test It! (30 sec)
1. Open http://localhost:3000
2. Sign up for an account
3. Go to "Predict" page
4. Enter: "I was charged twice for my subscription"
5. Click "Predict"
6. See AI classification! 🎉

## 🐛 Troubleshooting

**Backend won't start:**
```bash
# Check if model exists
ls models/smartsupport_model/model.pt

# If missing, download it (see MODEL_DOWNLOAD.md)
```

**Frontend can't connect:**
```bash
# Check backend is running
curl http://localhost:8000/health

# Should return: {"status":"healthy"}
```

**Model loading error:**
```bash
# Verify model file
python -c "import torch; torch.load('models/smartsupport_model/model.pt', map_location='cpu')"
```

## 🌐 Deploy for Free

See **DEPLOY.md** for step-by-step deployment to:
- Render (backend)
- Vercel (frontend)
- MongoDB Atlas (database)

All 100% FREE! 🎉

## 📚 More Info

- **README.md** - Full documentation
- **DEPLOY.md** - Deployment guide
- **MODEL_DOWNLOAD.md** - Model download options

## 🎯 Next Steps

1. ✅ Get it running locally
2. 📤 Deploy to Render + Vercel
3. 🗄️ Add MongoDB for ticket storage
4. 🎨 Customize the UI
5. 🚀 Share with the world!

Happy coding! 🚀
