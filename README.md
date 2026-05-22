🚀 QuotaGuard AI Bot

Intelligent AI failover system for Telegram bots with automatic quota recovery, model fallback, and resilient LLM orchestration.

<p align="center"> <img src="https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python"> <img src="https://img.shields.io/badge/FastAPI-Backend-green?style=for-the-badge&logo=fastapi"> <img src="https://img.shields.io/badge/Telegram-Bot-blue?style=for-the-badge&logo=telegram"> <img src="https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker"> <img src="https://img.shields.io/badge/AI-Gemini-orange?style=for-the-badge"> </p>
✨ Features

✅ Automatic AI provider fallback
✅ Handles HTTP 429 quota exhaustion
✅ Smart retry with exponential backoff
✅ Telegram chatbot integration
✅ Multi-model orchestration workflow
✅ SQLite persistent cooldown tracking
✅ FastAPI backend architecture
✅ Docker deployment ready
✅ GitHub Actions CI/CD included
✅ Production-friendly structure

📸 Preview
Telegram AI Assistant

API Health Dashboard

Quota Recovery Workflow

🧠 How It Works

QuotaGuard continuously monitors AI provider responses.

When a provider returns:

HTTP 429 - RESOURCE_EXHAUSTED

The system will:

Detect quota exhaustion
Activate cooldown timer
Retry with exponential backoff
Automatically switch to backup AI models
Preserve user conversation context
Restore original provider when available
⚡ Architecture
Telegram User
      │
      ▼
Telegram Bot API
      │
      ▼
 FastAPI Backend
      │
 ┌────┴────┐
 ▼         ▼
Gemini   Backup AI
Primary   Providers
      │
      ▼
SQLite State Manager
🛠 Tech Stack
Technology	Usage
Python	Core backend
FastAPI	API framework
Telegram Bot API	Messaging interface
SQLite	State persistence
Docker	Container deployment
GitHub Actions	CI/CD
Gemini API	AI inference
📦 Installation
Clone Repository
git clone https://github.com/YOUR_USERNAME/quota-guard-ai-bot.git
cd quota-guard-ai-bot
Install Dependencies
pip install -r requirements.txt
Setup Environment

Create .env

TELEGRAM_BOT_TOKEN=your_token
GEMINI_API_KEY=your_api_key
Run Application
python app.py
🐳 Docker
docker build -t quotaguard .
docker run -p 8000:8000 quotaguard
🔄 AI Recovery Workflow
try:
    response = primary_model.generate(prompt)
except QuotaExceeded:
    activate_cooldown()
    response = fallback_model.generate(prompt)
📁 Project Structure
quota-guard-ai-bot/
│
├── app/
│   ├── api/
│   ├── providers/
│   ├── storage/
│   └── bot/
│
├── screenshots/
├── Dockerfile
├── requirements.txt
├── README.md
└── .github/workflows/
🚀 Deployment

Supported platforms:

Railway
Render
VPS
Docker
Fly.io
📈 Future Improvements
 OpenAI fallback provider
 Claude integration
 AI load balancing
 Redis caching
 Grafana monitoring
 Admin dashboard
 Kubernetes deployment
🤝 Contributing

Pull requests are welcome.

For major changes:

Fork repository
Create feature branch
Commit changes
Open pull request
📜 License

MIT License

⭐ Support

If you like this project:

Star the repository ⭐
Fork the project 🍴
Share with developers 🚀
👨‍💻 Author

Dwi Farisco Afandi
