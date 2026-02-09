# AI Agent - Customer Service Chatbot 🤖

A friendly AI-powered customer service chatbot built with Django and integrated with OpenRouter AI. This application allows users to have interactive conversations with an AI assistant designed to help with ecommerce customer service inquiries.

## 📋 Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [API Endpoints](#api-endpoints)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## ✨ Features

- 💬 **Real-time Chat Interface** - Clean and responsive chat UI with smooth animations
- 🧠 **AI-Powered Responses** - Uses DeepSeek AI model via OpenRouter API for intelligent responses
- 💾 **Conversation History** - Stores all chat messages in MySQL database
- 🔄 **Session Management** - Maintains separate conversations for different users
- 🎨 **Beautiful UI** - Modern design with Tailwind CSS and Font Awesome icons
- 🧹 **Clear Chat** - Option to delete conversation history
- 📱 **Responsive Design** - Works seamlessly on desktop and mobile devices

## 🛠️ Technologies Used

- **Backend Framework:** Django 5.2
- **Database:** MySQL
- **AI API:** OpenRouter (DeepSeek R1 model)
- **Frontend:** HTML, Tailwind CSS, JavaScript
- **Python Libraries:**
  - `django` - Web framework
  - `python-decouple` - Environment variable management
  - `requests` - HTTP library for API calls
  - `mysqlclient` - MySQL database connector

## 📦 Prerequisites

Before you begin, make sure you have the following installed on your computer:

1. **Python 3.8 or higher** - [Download Python](https://www.python.org/downloads/)
2. **MySQL Server** - [Download MySQL](https://dev.mysql.com/downloads/mysql/)
3. **pip** - Python package installer (comes with Python)
4. **Git** (optional) - For cloning the repository

## 🚀 Installation

Follow these steps to set up the project on your local machine:

### Step 1: Clone or Download the Project

If you have Git installed:

```bash
git clone <your-repository-url>
cd ai_agent
```

Or download the project as a ZIP file and extract it.

### Step 2: Create a Virtual Environment (Recommended)

A virtual environment keeps your project dependencies isolated from other Python projects.

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate
```

### Step 3: Install Required Packages

```bash
pip install django python-decouple requests mysqlclient
```

### Step 4: Set Up MySQL Database

1. Open MySQL and create a new database:

```sql
CREATE DATABASE ai_agent_db;
```

2. Make sure your MySQL server is running on `localhost:3306` with the credentials:
   - **Username:** `root`
   - **Password:** _(leave empty or update in `settings.py`)_

## ⚙️ Configuration

### Step 1: Get Your OpenRouter API Key

1. Visit [OpenRouter.ai](https://openrouter.ai/)
2. Sign up for a free account
3. Navigate to the API Keys section
4. Create a new API key and copy it

### Step 2: Create Environment File

1. In the `ai_agent` folder (the one containing `settings.py`), create a file named `.env`
2. Add your OpenRouter API key to this file:

```env
OPENROUTER_API_KEY=your_api_key_here
```

**Important:** Replace `your_api_key_here` with your actual API key.

### Step 3: Run Database Migrations

Migrations create the necessary database tables for your application.

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 4: Create an Admin User (Optional)

If you want to access the Django admin panel:

```bash
python manage.py createsuperuser
```

Follow the prompts to create your admin account.

## ▶️ Running the Application

### Start the Development Server

```bash
python manage.py runserver
```

You should see output like:

```
Starting development server at http://127.0.0.1:8000/
```

### Access the Application

Open your web browser and go to:

- **Chat Interface:** http://127.0.0.1:8000/
- **Admin Panel:** http://127.0.0.1:8000/admin/ (if you created a superuser)

## 📁 Project Structure

```
ai_agent/
│
├── ai_agent/                 # Main project configuration
│   ├── __init__.py
│   ├── settings.py          # Django settings & configurations
│   ├── urls.py              # Main URL routing
│   ├── wsgi.py              # WSGI configuration
│   ├── asgi.py              # ASGI configuration
│   └── .env                 # Environment variables (API keys)
│
├── backend/                  # Main application
│   ├── migrations/          # Database migration files
│   ├── templates/           # HTML templates
│   │   └── chat.html        # Chat interface template
│   ├── __init__.py
│   ├── admin.py             # Admin panel configuration
│   ├── apps.py              # App configuration
│   ├── models.py            # Database models (ChatMessage)
│   ├── views.py             # View functions (chat logic)
│   └── urls.py              # App URL routing
│
├── manage.py                # Django management script
└── README.md                # This file
```

## 🔍 How It Works

### 1. **User Opens Chat**

- A unique session ID is created for each user
- Previous chat history for that session is loaded from the database

### 2. **User Sends a Message**

- The message is saved to the database with the session ID
- All previous messages in the session are retrieved
- Messages are sent to the OpenRouter API along with a system prompt

### 3. **AI Responds**

- The AI (DeepSeek model) generates a response based on the conversation history
- The response is saved to the database
- The response is displayed in the chat interface

### 4. **Conversation Continues**

- The AI maintains context from previous messages
- Users can clear chat history at any time

### Database Model

The `ChatMessage` model stores:

- **session_id**: Unique identifier for each chat session
- **role**: Either "user" or "assistant"
- **message**: The actual message text
- **timestamp**: When the message was created

## 🔌 API Endpoints

The application provides these internal API endpoints:

| Endpoint             | Method | Description                        |
| -------------------- | ------ | ---------------------------------- |
| `/`                  | GET    | Main chat interface                |
| `/api/send-message/` | POST   | Send a message and get AI response |
| `/api/clear-chat/`   | POST   | Clear chat history for a session   |

## 🐛 Troubleshooting

### Issue: "No module named 'mysqlclient'"

**Solution:** Install the MySQL client:

```bash
pip install mysqlclient
```

On Windows, if this fails, you may need to install Microsoft Visual C++ Build Tools.

### Issue: "Access denied for user 'root'@'localhost'"

**Solution:** Update your MySQL credentials in `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ai_agent_db',
        'USER': 'your_mysql_username',
        'PASSWORD': 'your_mysql_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### Issue: "API Error: 401"

**Solution:** Check that your `.env` file contains the correct OpenRouter API key.

### Issue: Database doesn't exist

**Solution:** Make sure you created the database in MySQL:

```sql
CREATE DATABASE ai_agent_db;
```

### Issue: Port 8000 is already in use

**Solution:** Either stop the other application using port 8000, or run Django on a different port:

```bash
python manage.py runserver 8080
```

## 📝 Customization

### Change the AI Model

Edit `backend/views.py` and modify the `model` parameter in the API call:

```python
"model": "deepseek/deepseek-r1-0528:free",  # Change to another model
```

### Customize the AI Behavior

Edit the system prompt in `backend/views.py`:

```python
{
    "role": "system",
    "content": """Your custom instructions here"""
}
```

### Modify the UI

Edit `backend/templates/chat.html` to change the appearance and functionality of the chat interface.

## 📄 License

This project is open source and available for educational purposes.

## 🤝 Contributing

Feel free to fork this project and submit pull requests with improvements!

## 📧 Support

If you encounter any issues or have questions, please create an issue in the repository.

---

**Happy Chatting! 🎉**
