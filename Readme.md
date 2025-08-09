# Fin-Minder: AI-Powered Payment Reminder Agent

![Fin-Minder Banner](https://placehold.co/1200x300/4f46e5/ffffff?text=Fin-Minder%0AAI-Powered%20Payment%20Reminder)

A sophisticated, multi-channel communication platform engineered to streamline and automate the process of sending personalized payment reminders using generative AI.

---

## 📜 AI Agents Hackathon Submission

- **Project Title:** Fin-Minder: AI-Powered Payment Reminder Agent  
- **Team Name:** Hello World  
- **Team Members:** Vishwasjeet Kumar Gupta, Tushar Kumar Chamlikar, Nishu Kumar  
- **Submission Date:** August 10, 2025  

---

## 📜 Abstract

The AI-Powered Payment Reminder System, **Fin-Minder**, is a sophisticated, multi-channel communication platform engineered to streamline and automate the process of sending payment reminders. By integrating APIs like **Twilio**, **SendGrid**, and **ElevenLabs**, it delivers notifications through SMS, email, and voice calls.

A key innovation is its **OpenAI-powered** personalized messages, making customer interactions more human-like. The system has:

- **Python (Flask) Backend** for logic & orchestration  
- **React (Vite) Frontend** for user interaction  

This document covers objectives, architecture, features, and implementation.

---

## 🎯 Introduction

### 1.1 Problem Statement
Manual payment tracking and reminders are time-consuming, prone to error, and often lack personalization. Generic automated messages are ignored, delaying payments.

### 1.2 Project Objective
- **Automate Communication:** No manual follow-up needed  
- **Personalize Messaging:** AI-generated human-like messages  
- **Multi-Channel Delivery:** SMS, Email, Voice  
- **Enhance Customer Experience:** Friendly and professional reminders  
- **Improve Efficiency:** Reduce admin load, faster payment cycles  

---

## 🏗️ System Architecture and Design

### 2.1 Architectural Overview

**Frontend (Client):**  
- React + Vite SPA  
- Tailwind CSS for styling  
- Captures reminder details and sends API requests to backend  

**Backend (Server):**  
- Python Flask REST API  
- Receives data, generates personalized content, sends via multiple APIs

---

### 2.2 Workflow

1. **User** → React Frontend → **POST `/reminders`**  
2. **Backend** orchestrates:
   - **OpenAI API:** Create personalized SMS text  
   - **Twilio Messaging API:** Send SMS  
   - **SendGrid API:** Send HTML email  
   - **ElevenLabs API:** Generate voice note  
   - **Twilio Voice API:** Make voice call  

---

## ✨ Core Features

### 3.1 Automated Email Reminders
- Professional, responsive HTML emails via SendGrid  
- Branding with Fin-Minder logo  
- Dynamic content for amount & due date  

### 3.2 AI-Personalized SMS Reminders
- OpenAI GPT-4o-mini for concise, polite text  
- Dynamic prompts for context-aware messaging  

### 3.3 Automated Voice Call Reminders
- Twilio Voice API for critical reminders  
- Reads payment details via TTS or pre-recorded audio  

### 3.4 High-Fidelity Voice Note Generation
- ElevenLabs for human-like speech  
- Attach to emails for unique customer experience  

---

## 🛠️ Technology Stack

| Category         | Technology / Service       | Purpose |
|------------------|----------------------------|---------|
| Backend          | Python, Flask              | API & orchestration |
| Frontend         | React, Vite, Tailwind CSS  | SPA UI |
| AI Language Model| OpenAI (GPT-4o-mini)       | Generate personalized text |
| Email Delivery   | SendGrid                   | Transactional HTML email delivery |
| SMS & Voice      | Twilio                     | Programmable SMS and voice calls |
| Voice Synthesis  | ElevenLabs                 | High-fidelity audio generation |

---

## 🚀 Installation & Usage

### 5.1 Prerequisites
- Python 3.8+ & pip  
- Node.js 16+ & npm  
- Git  

---

### 5.2 Clone Repository
```bash
git clone https://github.com/TusharChamlikar/AI-AGENT.git
cd AI-AGENT
```

---

### 5.3 Backend Setup
```bash
cd backend
pip install -r requirements.txt
python app.py
```
Backend runs at: **http://127.0.0.1:5000**

---

### 5.4 Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Frontend runs at: **http://localhost:5173**

---

## 🔑 Environment Variables (\`.env\`)

```env
# Twilio
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=+12345678901

# SendGrid
SENDGRID_API_KEY=SG.xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
FROM_EMAIL=your-email@example.com

# ElevenLabs
ELEVENLABS_API_KEY=your_elevenlabs_api_key
ELEVENLABS_VOICE_ID=your_chosen_voice_id

# OpenAI
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```
> Phone numbers must follow E.164 format (\`+<countrycode><number>\`)

---

## 📈 Example Request

**POST \`/reminders\`**
```json
{
  "recipient_name": "John Doe",
  "phone": "+911234567890",
  "email": "john@example.com",
  "amount": "3250.00",
  "due_date": "2025-08-20",
  "channels": ["sms", "email", "voice"]
}
```

---

## 📦 Suggested Project Structure

```
AI-AGENT/
├─ backend/
│  ├─ app.py
│  ├─ requirements.txt
│  ├─ services/
│  │  ├─ openai_service.py
│  │  ├─ twilio_service.py
│  │  ├─ sendgrid_service.py
│  │  ├─ elevenlabs_service.py
│  ├─ routes/
│  │  └─ reminders.py
├─ frontend/
│  ├─ src/
│  │  ├─ App.jsx
│  │  ├─ components/
│  │  └─ styles/
└─ README.md
```

---

## 📊 Future Scope

- **Interactive Voice Response (IVR):** Allow customers to respond via keypad  
- **Dashboard & Analytics:** Delivery/open rates, payment success rates  

---

## 🧾 Credits

**Hello World Team**  
- Vishwasjeet Kumar Gupta  
- Tushar Kumar Chamlikar  
- Nishu Kumar  

---

**License:** MIT
