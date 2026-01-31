# Frontend - Student Dropout Risk Prediction System

## Overview
React-based frontend for the Student Dropout Risk Prediction System. Provides an intuitive interface for analyzing student data and predicting dropout risk.

## Features
- 🔍 Student search by roll number
- 📊 Comprehensive student profile display
- 🎯 Real-time dropout risk prediction
- 📈 Visual risk factor breakdown
- 💡 Actionable intervention recommendations

## Tech Stack
- React 18
- Vite
- CSS3 (Custom styling)

## Setup

### Prerequisites
- Node.js 16+ or Yarn

### Installation

1. Install dependencies:
```bash
yarn install
```

2. Create `.env` file:
```bash
cp .env.example .env
```

3. Update `.env` with your backend URL:
```
VITE_API_URL=http://localhost:8000
```

### Development

Run development server:
```bash
yarn dev
```

The app will be available at `http://localhost:5173`

### Build

Create production build:
```bash
yarn build
```

Preview production build:
```bash
yarn preview
```

## Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── SearchSection/   # Student search input
│   ├── StudentProfileCard/  # Static student info
│   ├── OngoingDataCard/     # Dynamic performance data
│   ├── PredictionButton/    # Trigger prediction
│   ├── RiskAlertCard/       # Risk level display
│   ├── RiskFactorsCard/     # Risk factors breakdown
│   ├── RecommendationsCard/ # Intervention suggestions
│   └── Loader/              # Loading spinner
├── pages/               # Page components
│   └── Home.jsx         # Main application page
├── services/            # API integration
│   └── api.js           # API calls
└── styles/              # Global styles
    └── global.css
```

## Usage Flow

1. **Search**: Enter student roll number
2. **Analyze**: View student profile and performance data
3. **Predict**: Click "Generate Risk Prediction" button
4. **Review**: See risk level, factors, and recommendations
5. **Act**: Use action buttons to take interventions

## API Integration

The frontend communicates with the backend via REST API:

- `GET /api/student/:rollNo` - Fetch student data
- `POST /api/predict/:rollNo` - Get dropout prediction

## Customization

### Colors
Edit CSS variables in `src/styles/global.css`:
```css
:root {
  --primary-color: #667eea;
  --secondary-color: #764ba2;
  --danger-color: #ef4444;
  --warning-color: #f59e0b;
  --success-color: #10b981;
}
```

### Components
Each component is self-contained with its own JSX and CSS files for easy customization.

## Browser Support
- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
