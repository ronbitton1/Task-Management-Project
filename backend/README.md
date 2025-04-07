# Voltify Task Manager API

Voltify is a Flask-based task management API enhanced with OpenAI for smart task insights and integrated with Telegram for real-time notifications. It supports user authentication, CRUD operations on tasks, and AI-powered features like task recommendations and weekly summaries.

---

## 🚀 Features

- 🧑‍💼 User authentication (register, login, logout)
- ✅ Task CRUD operations
- 🤖 AI recommendations via OpenAI (task estimation & categorization)
- 📬 Telegram notifications for new/completed tasks
- 📊 Weekly smart summary via OpenAI + Telegram
- ⚙️ Session-based security with Flask
- 🧪 Modular architecture using Blueprints and logic helpers

---

## 📁 Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/your-username/voltify-backend.git
cd voltify-backend
```

### 2. Create a `.env` file
```
MONGO_URI=mongodb://localhost:27017/task_management_db
SECRET_KEY=your_secret
OPENAI_API_KEY=your_openai_key
TELEGRAM_BOT_TOKEN=your_telegram_token
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
python app.py
```

---

## 📚 API Endpoints

### 🔐 Auth
- `POST /api/auth/register` – Register a new user
- `POST /api/auth/login` – Log in
- `POST /api/auth/logout` – Log out
- `GET /api/auth/me` – Get current user

### 📝 Tasks
- `GET /api/tasks` – Get all tasks (with optional filters `status`/`category`)
- `POST /api/tasks` – Create new task
- `GET /api/tasks/<task_id>` – Get specific task
- `PUT /api/tasks/<task_id>` – Update task
- `DELETE /api/tasks/<task_id>` – Delete task
- `POST /api/tasks/update-chat-id` – Update Telegram chat ID
- `POST /api/tasks/weekly-summary` – Trigger AI-generated summary for open tasks

### 🧠 AI
- `POST /api/ai/recommend` – Get AI recommendation based on task description

---

## 🔐 Security Considerations

- All user endpoints are protected with session-based auth
- Inputs validated using helper functions (`validators.py`)
- Secrets are stored in `.env`
- CORS is enabled via `flask-cors`
- Cookie settings: `SESSION_COOKIE_SECURE = True`
- (Optional) You can add `Flask-Limiter` or logging via `Flask-Logging`

---

## 🎯 Custom Features

- **Telegram integration** for real-time task alerts & AI summaries
- **Weekly smart summary** using OpenAI GPT
- **Update chat ID endpoint** for flexible notifications

---

## 📦 Deployment Ready

- Structure supports Docker and AWS deployment (optional Dockerfile)
- Environment separation using `.env`
- Future-proof for frontend or mobile integration

---

## 📽️ Submission
- [ ] Push code to GitHub
- [ ] Record demo video
- [ ] Submit repo + video link by **April 8, 2025** to `matan@justvoltify.com`

---

## 🙌 Credits
Made with ❤️ by [Your Name]

