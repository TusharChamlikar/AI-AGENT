# AI-Powered Payment Reminder System

This project is an **AI-driven multi-channel payment reminder system** that sends notifications via **SMS, Email, Voice, and Calls** using services like **Twilio, ElevenLabsI**, and integrates AI-generated personalized messages using **OpenAI API**.

It includes:
- **Backend (Python)** for AI message generation, voice synthesis, and integration with APIs.
- **Frontend (React)** for managing reminders and user interactions.


---

## 🚀 Features
- Send **SMS** payment reminders using **Twilio**.
- Send **Email** reminders using **SendGrid**.
- Make **Voice Calls** using **Twilio**.
- Generate **human-like voice** reminders using **ElevenLabs**.
- Automatically **generate personalized reminder messages** with **OpenAI API**.



---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
    git clone https://github.com/TusharChamlikar/AI-AGENT.git

### 2️⃣ Backend Setup
    pip install -r requirements.txt
    python -m backend.app
 
### 3️⃣ Frontend Setup
    
    cd frontend/paymind
    npm install
    npm run dev

### 🔑 Environment Variables
    Create a .env file in the ai folder for backend configuration:

    TWILIO_ACCOUNT_SID=your_twilio_sid
    TWILIO_AUTH_TOKEN=your_twilio_auth_token
    TWILIO_PHONE_NUMBER=your_twilio_number

    SENDGRID_API_KEY=your_sendgrid_api_key
    ELEVENLABS_API_KEY=your_elevenlabs_api_key
    OPENAI_API_KEY=your_openai_api_key

### 🛠 Tech Stack
    Backend: Python (Flask / FastAPI), OpenAI API

    Frontend: React + Vite

    Messaging & Voice: Twilio, SendGrid, ElevenLabs

  

