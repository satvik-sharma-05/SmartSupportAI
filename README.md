# 🎯 SmartSupport AI

AI-powered support ticket classification and prioritization system. Automatically categorizes tickets and assigns priority levels using intelligent classification.

**Live Demo:**
- 🌐 Frontend: https://smart-support-ai-sandy.vercel.app/
- 🔌 Backend API: https://smartsupportai-backend.onrender.com
- 📚 API Docs: https://smartsupportai-backend.onrender.com/docs

---

## ✨ Features

- **Automatic Classification**: Categorizes tickets into Billing, Technical, Account, or General
- **Priority Assignment**: Assigns High, Medium, or Low priority based on urgency
- **Real-time Predictions**: Instant classification with confidence scores
- **Modern UI**: Clean, responsive interface built with React + Tailwind CSS
- **RESTful API**: FastAPI backend with automatic documentation
- **Free Deployment**: Optimized for free tier hosting (Render + Vercel)

---

## 🚀 Quick Start

### Try the Live Demo

1. Visit https://smart-support-ai-sandy.vercel.app/
2. Sign up for an account
3. Go to "Predict" page
4. Enter a support ticket (e.g., "I was charged twice for my subscription")
5. Click "Predict" to see AI classification

### Example Predictions

**Billing Issue:**
```
Input: "I was charged twice for my subscription this month"
Output: Category=Billing (92%), Priority=High (85%)
```

**Technical Issue:**
```
Input: "The application crashes when I upload files"
Output: Category=Technical (88%), Priority=High (90%)
```

**Account Question:**
```
Input: "How do I change my password?"
Output: Category=Account (85%), Priority=Medium (75%)
```

---

## 🏗️ Architecture

### Tech Stack

**Frontend:**
- React 18 + Vite
- Tailwind CSS
- React Router
- Axios

**Backend:**
- FastAPI (Python)
- Rule-based classifier (optimized for free tier)
- Pydantic for validation
- CORS enabled

**Deployment:**
- Frontend: Vercel (Free)
- Backend: Render (Free Tier)

### How It Works

1. User submits a support ticket through the web interface
2. Frontend sends POST request to `/predict` endpoint
3. Backend analyzes text using keyword-based classification
4. Returns category, priority, and confidence scores
5. Frontend displays results with visual indicators

---

## 📦 Installation

### Prerequisites

- Python 3.11+
- Node.js 18+
- npm or yarn

### Backend Setup

```bash
# Clone repository
git clone https://github.com/satvik-sharma-05/SmartSupportAI.git
cd SmartSupportAI

# Install Python dependencies
pip install -r requirements-minimal.txt

# Run backend server
uvicorn app.main_lightweight:app --host 0.0.0.0 --port 8000
```

Backend will be available at http://localhost:8000

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create .env file
echo "VITE_API_URL=http://localhost:8000" > .env

# Run development server
npm run dev
```

Frontend will be available at http://localhost:5173

---

## 🔌 API Usage

### Health Check

```bash
curl https://smartsupportai-backend.onrender.com/health
```

Response:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "model": "rule-based-v1"
}
```

### Predict Ticket

```bash
curl -X POST https://smartsupportai-backend.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{
    "text": "I was charged twice for my subscription"
  }'
```

Response:
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

### API Documentation

Interactive API docs available at:
- Swagger UI: https://smartsupportai-backend.onrender.com/docs
- ReDoc: https://smartsupportai-backend.onrender.com/redoc

---

## 🎨 Screenshots

### Homepage
Clean landing page with feature highlights

### Prediction Interface
Simple form to submit tickets and view AI predictions

### Results Display
Visual representation of category and priority with confidence scores

---

## 📊 Classification Details

### Categories

- **Billing**: Payment, charges, subscriptions, refunds
- **Technical**: Bugs, errors, crashes, performance issues
- **Account**: Login, password, access, verification
- **General**: Questions, features, information requests

### Priority Levels

- **High**: Urgent issues requiring immediate attention
- **Medium**: Important issues that should be addressed soon
- **Low**: General questions or non-urgent requests

### Accuracy

The rule-based classifier achieves approximately 75-80% accuracy on common support tickets. For production use with higher accuracy requirements, consider upgrading to the ML model version.

---

## 🚀 Deployment

### Deploy Your Own Instance

#### Backend (Render)

1. Fork this repository
2. Create account on [Render](https://render.com)
3. Create new Web Service
4. Connect your GitHub repository
5. Configure:
   - **Build Command**: `pip install -r requirements-minimal.txt`
   - **Start Command**: `bash start-lightweight.sh`
   - **Instance Type**: Free
6. Deploy!

#### Frontend (Vercel)

1. Create account on [Vercel](https://vercel.com)
2. Import your GitHub repository
3. Configure:
   - **Framework**: Vite
   - **Root Directory**: `frontend`
   - **Environment Variable**: `VITE_API_URL=https://your-backend.onrender.com`
4. Deploy!

---

## 🛠️ Development

### Project Structure

```
SmartSupportAI/
├── app/                          # Backend application
│   ├── main_lightweight.py       # FastAPI app (lightweight)
│   ├── inference_lightweight.py  # Rule-based classifier
│   └── database.py               # Database utilities (optional)
├── frontend/                     # React frontend
│   ├── src/
│   │   ├── pages/               # Page components
│   │   ├── components/          # Reusable components
│   │   └── services/            # API services
│   └── package.json
├── requirements-minimal.txt      # Python dependencies (lightweight)
├── start-lightweight.sh          # Startup script
└── README.md
```

### Running Tests

```bash
# Backend tests
pytest

# Frontend tests
cd frontend
npm test
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Frontend powered by [React](https://react.dev/) and [Tailwind CSS](https://tailwindcss.com/)
- Deployed on [Render](https://render.com) and [Vercel](https://vercel.com)

---

## 📧 Contact

**Satvik Sharma**
- GitHub: [@satvik-sharma-05](https://github.com/satvik-sharma-05)
- Project Link: [https://github.com/satvik-sharma-05/SmartSupportAI](https://github.com/satvik-sharma-05/SmartSupportAI)

---

## 🔮 Future Enhancements

- [ ] Add ML model version with transformer-based classification
- [ ] Implement user authentication and ticket history
- [ ] Add analytics dashboard
- [ ] Support for multiple languages
- [ ] Email integration for automatic ticket processing
- [ ] Mobile app version

---

**⭐ If you find this project useful, please consider giving it a star!**
