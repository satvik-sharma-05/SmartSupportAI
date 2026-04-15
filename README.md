# SmartSupport AI

AI-powered support ticket classification system using DeBERTa transformer model. Automatically categorizes tickets (Billing, Technical, Account, General) and assigns priority levels (High, Medium, Low).

## 🚀 Features

- **AI Classification**: 73% accuracy using microsoft/deberta-v3-base
- **Multi-task Learning**: Predicts both category and priority
- **Real-time API**: FastAPI backend with <2s inference time
- **Modern UI**: React + Tailwind CSS premium interface
- **Authentication**: JWT-based user authentication
- **MongoDB**: Ticket history and analytics

## 📋 Tech Stack

**Backend:**
- Python 3.8+
- FastAPI
- PyTorch
- Transformers (Hugging Face)
- MongoDB

**Frontend:**
- React 18
- Vite
- Tailwind CSS
- Axios

**ML Model:**
- microsoft/deberta-v3-base (184M parameters)
- Trained on 8,000 real support tickets
- 73.33% category accuracy, 66.17% priority accuracy

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- Node.js 16+
- MongoDB (optional - for ticket storage)

### Backend Setup

```bash
# Clone repository
git clone <your-repo-url>
cd SmartSupportAI

# Install Python dependencies
pip install -r requirements.txt

# Download the trained model (703MB)
# Download from Google Drive:
wget --no-check-certificate 'https://drive.google.com/uc?export=download&id=1Igb0dGI6-HlyccZWe8F82c2XA5m7TyZG' -O models/smartsupport_model/model.pt

# Or download manually from:
# https://drive.google.com/file/d/1Igb0dGI6-HlyccZWe8F82c2XA5m7TyZG/view
# Place it in: models/smartsupport_model/model.pt

# Create .env file
cp .env.example .env
# Edit .env with your MongoDB URI (optional)

# Run backend
uvicorn app.main:app --reload
```

Backend runs on: http://localhost:8000

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env

# Run frontend
npm run dev
```

Frontend runs on: http://localhost:3000

## 🌐 Free Deployment Options

### Backend Deployment

**Option 1: Render (Recommended)**
1. Create account at [render.com](https://render.com)
2. Connect your GitHub repository
3. Create new Web Service
4. Build command: `pip install -r requirements.txt`
5. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
6. Add environment variables (MongoDB URI if needed)

**Option 2: Railway**
1. Create account at [railway.app](https://railway.app)
2. Deploy from GitHub
3. Add start command in Procfile
4. Set environment variables

**Option 3: Fly.io**
```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Deploy
fly launch
fly deploy
```

### Frontend Deployment

**Option 1: Vercel (Recommended)**
```bash
cd frontend
npm install -g vercel
vercel
```

**Option 2: Netlify**
```bash
cd frontend
npm run build
# Drag dist/ folder to netlify.com
```

**Option 3: GitHub Pages**
```bash
cd frontend
npm run build
# Deploy dist/ folder to gh-pages branch
```

### Database (Optional)

**Free MongoDB Options:**
- MongoDB Atlas (512MB free tier)
- Railway MongoDB (5GB free)

## 📁 Project Structure

```
SmartSupportAI/
├── app/                    # Backend API
│   ├── main.py            # FastAPI app
│   ├── inference.py       # ML inference
│   ├── model_loader.py    # Model loading
│   ├── database.py        # MongoDB connection
│   └── utils.py           # Utilities
├── ml/                     # ML training code
│   ├── config.py          # Model configuration
│   ├── model.py           # Model architecture
│   └── train.py           # Training script
├── models/                 # Trained models
│   └── smartsupport_model/
│       ├── model.pt       # Model weights (703MB)
│       └── metadata.json  # Model metadata
├── frontend/              # React frontend
│   ├── src/
│   │   ├── pages/        # Page components
│   │   ├── components/   # Reusable components
│   │   ├── services/     # API services
│   │   └── context/      # React context
│   └── public/
├── data/                  # Training data
├── .env                   # Environment variables
├── requirements.txt       # Python dependencies
├── Procfile              # Deployment config
└── README.md             # This file
```

## 🔧 Configuration

### Environment Variables

**Backend (.env):**
```env
MONGODB_URI=mongodb://localhost:27017/smartsupport
SECRET_KEY=your-secret-key-here
MODEL_PATH=models/smartsupport_model
```

**Frontend (.env):**
```env
VITE_API_URL=http://localhost:8000
```

## 📊 API Endpoints

### Authentication
- `POST /signup` - Create new user
- `POST /login` - User login

### Predictions
- `POST /predict` - Classify ticket
  ```json
  {
    "text": "I was charged twice for my subscription"
  }
  ```
  Response:
  ```json
  {
    "category": "Billing",
    "category_confidence": 0.87,
    "priority": "High",
    "priority_confidence": 0.76,
    "inference_time_ms": 1250
  }
  ```

### Analytics
- `GET /statistics` - Get ticket statistics
- `GET /tickets` - Get ticket history
- `GET /health` - Health check

## 🎯 Model Performance

| Metric | Score |
|--------|-------|
| Category Accuracy | 73.33% |
| Priority Accuracy | 66.17% |
| Billing Recall | 100% |
| Account Recall | 88% |
| Technical Recall | 76% |
| Inference Time | <2s |

### Category Performance
- **Billing**: 86% precision, 100% recall
- **Account**: 56% precision, 88% recall
- **Technical**: 81% precision, 76% recall
- **General**: 91% precision, 29% recall

## 🚨 Known Issues

1. **Model predictions showing low confidence (~30%)**
   - The current model needs retraining with more epochs
   - Use the training script in `ml/train.py` on Google Colab
   - Expected improvement: 30% → 75% accuracy

2. **MongoDB connection warnings**
   - App works without MongoDB (predictions only)
   - To enable storage, set MONGODB_URI in .env

## 🔄 Retraining the Model

If you need to retrain the model:

1. Open Google Colab
2. Upload `ml/train.py`
3. Enable GPU (Runtime → Change runtime type → GPU)
4. Run the training script
5. Download `best_model.pt`
6. Replace `models/smartsupport_model/model.pt`

## 📝 License

MIT License - see LICENSE file

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📧 Support

For issues and questions, please open a GitHub issue.

## 🙏 Acknowledgments

- Hugging Face Transformers
- Microsoft DeBERTa
- Kaggle datasets for training data
- FastAPI and React communities
