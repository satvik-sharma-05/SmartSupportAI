# SmartSupport AI - Frontend

Production-grade SaaS web application for SmartSupport AI ticket classification system.

## 🎯 Features

- **Modern Landing Page**: Professional homepage with glassmorphism design
- **Authentication System**: Full login/signup flow with validation
- **Dashboard**: Analytics with charts (Recharts)
- **Prediction Interface**: Real-time ticket classification
- **Responsive Design**: Mobile-first approach with Tailwind CSS
- **Smooth Animations**: Framer Motion for polished UX
- **Toast Notifications**: User feedback with react-hot-toast

## 🛠️ Tech Stack

- **React 18** - Latest React with hooks
- **Vite** - Fast build tool
- **Tailwind CSS** - Utility-first CSS
- **React Router** - Client-side routing
- **Axios** - HTTP client
- **Recharts** - Chart library
- **Zustand** - State management
- **Framer Motion** - Animations
- **Lucide React** - Icon library

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure Environment

Create `.env` file:

```env
VITE_API_URL=http://localhost:8000
```

### 3. Start Development Server

```bash
npm run dev
```

The app will be available at `http://localhost:3000`

### 4. Build for Production

```bash
npm run build
```

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   └── ProtectedRoute.jsx
│   ├── context/
│   │   └── AuthContext.jsx
│   ├── layouts/
│   │   └── DashboardLayout.jsx
│   ├── pages/
│   │   ├── HomePage.jsx
│   │   ├── LoginPage.jsx
│   │   ├── SignupPage.jsx
│   │   ├── Dashboard.jsx
│   │   └── PredictPage.jsx
│   ├── services/
│   │   └── api.js
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css
├── package.json
├── vite.config.js
├── tailwind.config.js
└── postcss.config.js
```

## 🎨 Pages

### Homepage (/)
- Hero section with CTA
- Features showcase
- How it works
- Statistics
- Footer

### Login (/login)
- Email/password form
- Form validation
- Social login buttons
- Remember me option

### Signup (/signup)
- Full name, email, password
- Password strength indicator
- Confirm password
- Terms acceptance

### Dashboard (/dashboard) - Protected
- Stats cards (Total tickets, High priority, etc.)
- Category distribution (Pie chart)
- Priority distribution (Bar chart)
- Ticket trends (Line chart)
- Recent tickets table

### Predict (/predict) - Protected
- Ticket input textarea
- Example tickets
- Real-time prediction
- Confidence scores
- Category and priority display

## 🔐 Authentication

The frontend uses a mock authentication system. In production, replace with real backend auth:

1. Update `src/services/api.js`
2. Implement JWT token handling
3. Add refresh token logic
4. Connect to backend auth endpoints

## 🎨 Design System

### Colors
- Primary: Blue (600-700)
- Secondary: Indigo (600-700)
- Success: Green (500-600)
- Warning: Yellow (500-600)
- Error: Red (500-600)

### Components
- `.glass` - Glassmorphism effect
- `.card` - Standard card component
- `.btn-primary` - Primary button
- `.btn-secondary` - Secondary button
- `.input-field` - Form input

### Animations
- Fade in on mount
- Smooth transitions
- Hover effects
- Loading states

## 📊 Charts

Using Recharts for data visualization:

- **Pie Chart**: Category distribution
- **Bar Chart**: Priority distribution
- **Line Chart**: Ticket trends

## 🔌 API Integration

### Endpoints Used

```javascript
// Health check
GET /health

// Predict ticket
POST /predict
Body: { text: string }

// Get tickets
GET /tickets?limit=100

// Get predictions
GET /predictions?limit=100

// Get statistics
GET /statistics
```

### API Service

Located in `src/services/api.js`:

```javascript
import { apiService } from './services/api'

// Example usage
const result = await apiService.predictTicket(text)
const tickets = await apiService.getTickets(100)
const stats = await apiService.getStatistics()
```

## 🎯 Features Breakdown

### Authentication Flow
1. User enters credentials
2. Form validation
3. API call (mock)
4. Store token in localStorage
5. Redirect to dashboard

### Protected Routes
- Check authentication status
- Redirect to login if not authenticated
- Show loading state during check

### Dashboard Analytics
- Fetch statistics from API
- Display in cards and charts
- Real-time updates
- Responsive layout

### Ticket Prediction
1. User enters ticket text
2. Validation (min 10 chars)
3. API call to /predict
4. Display results with confidence
5. Save to database
6. Show success notification

## 🚀 Deployment

### Vercel (Recommended)

```bash
npm run build
vercel --prod
```

### Netlify

```bash
npm run build
netlify deploy --prod --dir=dist
```

### Docker

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
RUN npm install -g serve
CMD ["serve", "-s", "dist", "-l", "3000"]
```

## 🔧 Configuration

### Vite Config

```javascript
// vite.config.js
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': 'http://localhost:8000'
    }
  }
})
```

### Tailwind Config

```javascript
// tailwind.config.js
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      // Custom theme extensions
    }
  }
}
```

## 📱 Responsive Design

- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px

All components are fully responsive with mobile-first approach.

## 🎨 Customization

### Change Colors

Edit `tailwind.config.js`:

```javascript
theme: {
  extend: {
    colors: {
      primary: {
        500: '#your-color',
        600: '#your-color',
      }
    }
  }
}
```

### Add New Pages

1. Create page in `src/pages/`
2. Add route in `App.jsx`
3. Update navigation in `DashboardLayout.jsx`

### Modify Charts

Edit chart components in `Dashboard.jsx`:

```javascript
<PieChart>
  <Pie data={yourData} />
</PieChart>
```

## 🐛 Troubleshooting

### Port already in use

```bash
# Change port in vite.config.js
server: { port: 3001 }
```

### API connection failed

```bash
# Check .env file
VITE_API_URL=http://localhost:8000

# Ensure backend is running
cd ..
uvicorn app.main:app --reload
```

### Build errors

```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

## 📚 Resources

- [React Documentation](https://react.dev/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Vite](https://vitejs.dev/)
- [Recharts](https://recharts.org/)
- [Framer Motion](https://www.framer.com/motion/)

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## 📄 License

MIT License

---

**Built with ❤️ using React, Tailwind CSS, and modern web technologies**
