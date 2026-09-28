# Nivara AI — Investment Intelligence Platform

> **AI-powered investment intelligence built for India.**  
> Your personal Bloomberg Terminal + Zerodha + ChatGPT — all in one app, fully personalized.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=flat&logo=react)](https://react.dev)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## ✨ Features

| Feature | Description |
|---|---|
| 🤖 **AI Financial Advisor** | Claude-powered chat with full portfolio context |
| 📊 **Live Portfolio Tracking** | Real-time P&L via yfinance (NSE/BSE) |
| 💰 **Broker Cost Comparator** | Exact charges across 15 brokers — STT, GST, stamp duty |
| 📋 **Tax P&L Calculator** | STCG/LTCG with ITR-ready summary |
| 🎯 **Goal-Based Investing** | SIP planner with AI fund recommendations |
| 👁 **Watchlist & Alerts** | Price alerts via push/email/WhatsApp |
| 🔮 **What-If Simulator** | SIP growth, market crash, lump sum scenarios |
| 📰 **Portfolio News Feed** | Only news that impacts stocks you own |
| 🔌 **72 Platform Connectors** | Groww, Zerodha, NSDL, CDSL, unlisted & more |
| ⚡ **WebSocket Live Prices** | Real-time price streaming |

---

## 🏗️ Project Structure

```
nivara-ai/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── main.py             # App entry point, CORS, router registration
│   │   ├── config.py           # Settings (env vars, JWT config)
│   │   ├── database.py         # SQLAlchemy engine + session
│   │   ├── models/             # ORM models
│   │   │   ├── user.py
│   │   │   ├── portfolio.py
│   │   │   ├── goal.py
│   │   │   └── alert.py
│   │   ├── schemas/            # Pydantic request/response schemas
│   │   │   ├── user.py
│   │   │   ├── portfolio.py
│   │   │   ├── goal.py
│   │   │   └── alert.py
│   │   ├── routers/            # Route handlers
│   │   │   ├── auth.py
│   │   │   ├── portfolio.py
│   │   │   ├── market.py
│   │   │   ├── broker.py
│   │   │   ├── tax.py
│   │   │   ├── goals.py
│   │   │   ├── watchlist.py
│   │   │   ├── alerts.py
│   │   │   ├── news.py
│   │   │   ├── ai_chat.py
│   │   │   ├── briefing.py
│   │   │   └── websocket.py
│   │   ├── services/           # Business logic
│   │   │   ├── market_data.py
│   │   │   ├── broker_charges.py
│   │   │   ├── tax_calculator.py
│   │   │   ├── goal_calculator.py
│   │   │   └── ai_service.py
│   │   └── utils/
│   │       ├── auth.py         # JWT + password hashing
│   │       └── cache.py        # In-memory price cache (TTL)
│   ├── tests/
│   │   ├── test_auth.py
│   │   ├── test_portfolio.py
│   │   └── test_broker.py
│   ├── requirements.txt
│   ├── .env.example
│   └── Dockerfile
├── frontend/                   # React + Vite frontend
│   ├── src/
│   │   ├── main.jsx            # App entry point
│   │   ├── App.jsx             # Router + layout
│   │   ├── api/                # Axios API clients
│   │   │   ├── client.js       # Base axios instance + interceptors
│   │   │   ├── auth.js
│   │   │   ├── portfolio.js
│   │   │   ├── market.js
│   │   │   ├── broker.js
│   │   │   ├── goals.js
│   │   │   └── news.js
│   │   ├── components/
│   │   │   ├── layout/
│   │   │   │   ├── Sidebar.jsx
│   │   │   │   └── Topbar.jsx
│   │   │   └── ui/
│   │   │       ├── ScoreRing.jsx
│   │   │       ├── Sparkline.jsx
│   │   │       ├── ConfBar.jsx
│   │   │       ├── AlertBox.jsx
│   │   │       └── LoadingSpinner.jsx
│   │   ├── pages/
│   │   │   ├── Login.jsx
│   │   │   ├── Register.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Holdings.jsx
│   │   │   ├── Chat.jsx
│   │   │   ├── Briefing.jsx
│   │   │   ├── Risk.jsx
│   │   │   ├── BrokerCost.jsx
│   │   │   ├── TaxPL.jsx
│   │   │   ├── Goals.jsx
│   │   │   ├── Watchlist.jsx
│   │   │   ├── WhatIf.jsx
│   │   │   ├── News.jsx
│   │   │   └── Connect.jsx
│   │   ├── store/
│   │   │   ├── authStore.js    # Zustand auth store
│   │   │   └── portfolioStore.js
│   │   ├── hooks/
│   │   │   ├── useAuth.js
│   │   │   ├── usePrices.js    # WebSocket price hook
│   │   │   └── usePortfolio.js
│   │   └── styles/
│   │       └── globals.css
│   ├── public/
│   │   └── favicon.ico
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── .env.example
│   └── Dockerfile
├── nginx/
│   └── nginx.conf              # Reverse proxy config
├── docker-compose.yml          # One-command full stack
├── docker-compose.prod.yml     # Production override
├── .gitignore
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 20+
- Git

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/nivara-ai.git
cd nivara-ai
```

### 2. Backend setup
```bash
cd backend
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env — add your ANTHROPIC_API_KEY
uvicorn app.main:app --reload --port 8000
```

### 3. Frontend setup
```bash
cd frontend
npm install
cp .env.example .env.local
# Edit .env.local if needed
npm run dev
```

Open **http://localhost:5173** — the app is running.

---

## 🐳 Docker (Recommended)

```bash
# Copy environment files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env.local

# Edit backend/.env and add ANTHROPIC_API_KEY

# Start full stack
docker-compose up --build

# App runs on http://localhost:3000
```

---

## 🔑 Environment Variables

### Backend (`backend/.env`)
```env
SECRET_KEY=your-super-secret-jwt-key-change-this
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxx
DATABASE_URL=sqlite:///./nivara.db
ENVIRONMENT=development
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

### Frontend (`frontend/.env.local`)
```env
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
```

---

## 📡 API Reference

Full interactive docs at **http://localhost:8000/docs** (Swagger UI)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Register new user |
| POST | `/auth/login` | Login (returns JWT) |
| GET | `/auth/me` | Current user profile |
| GET | `/portfolio/holdings` | All holdings with live prices |
| GET | `/portfolio/summary` | P&L summary + sector allocation |
| POST | `/portfolio/holdings` | Add a holding |
| DELETE | `/portfolio/holdings/{id}` | Remove a holding |
| POST | `/broker/calculate` | Compare charges across all brokers |
| GET | `/market/price/{symbol}` | Live price for a symbol |
| GET | `/market/quote/{symbol}` | Full quote + fundamentals |
| GET | `/tax/summary` | STCG/LTCG tax summary |
| GET | `/goals` | All financial goals |
| POST | `/goals` | Create a goal |
| GET | `/watchlist` | Watchlist with live prices |
| POST | `/alerts` | Create price alert |
| GET | `/news/portfolio` | News for your holdings |
| POST | `/ai/chat` | AI advisor chat |
| GET | `/briefing/daily` | Personalized morning briefing |
| WS | `/ws/prices` | Live price WebSocket stream |

---

## 🧪 Running Tests

```bash
cd backend
pytest tests/ -v --cov=app
```

---

## 🌐 Production Deployment

### Using Docker Compose (recommended)
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### Manual (VPS / Cloud)
```bash
# Backend: use gunicorn with uvicorn workers
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# Frontend: build static files
cd frontend && npm run build
# Serve dist/ with nginx
```

---

## ⚖️ Disclaimer

> Nivara AI provides AI-assisted investment insights and market information for educational purposes only. It does **not** constitute certified financial advice. Always consult a SEBI-registered investment advisor before making investment decisions. Nivara AI is not a registered investment advisor or broker.

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.
