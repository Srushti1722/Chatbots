# 🧠 FastAPI Chatbot

A simple AI-style chatbot backend built with **FastAPI**, **SQLite**, and **Uvicorn**.  
It supports creating chat sessions, storing messages, and generating dummy AI replies.

---

## 🚀 Setup & Run Locally

### 1️⃣ Clone or Create the Project Folder
mkdir fastapi-chatbot
cd fastapi-chatbot
### 2️⃣ Create a Virtual Environment
python -m venv venv

Activate it:
- **Windows:** `venv\Scripts\activate`

### 3️⃣ Install Dependencies
pip install fastapi uvicorn sqlalchemy

### 4️⃣ Create Files
Make a file named **`main.py`** and paste chatbot code 
Example structure:
```
fastapi-chatbot/
│
|-- main.py
|-- database.py
|-- chatbot.db        ← auto-created after first run
└-- requirements.txt  ← optional
```
### 5️⃣ Run the Server
uvicorn main:app --reload
Server will start at:
```
http://127.0.0.1:8000
```
---
### 6️⃣ Test Endpoints in Postman
| Method | Endpoint | Description |
|--------|-----------|--------------|
| POST | `/sessions` | Create a new chat session |
| POST | `/sessions/{id}/messages` | Add user message |
| POST | `/sessions/{id}/llm-reply` | Generate AI reply |
| GET | `/sessions/{id}` | Retrieve all messages |
Use  **Header:** `Content-Type: application/json` **Body → raw → JSON** and add these 

### 7️⃣ Example API Flow
1. POST:-http://127.0.0.1:8000/session:- Create session → `/sessions` → `{ "user_name": "Srushti" }`  
2. POST:-http://127.0.0.1:8000/session/{id}/message:-Add message → `/sessions/1/messages` → `{ "sender": "Srushti", "text": "Hello!" }`  
3. POST:-http://127.0.0.1:8000/session/{id}/llm-reply:-Generate reply → `/sessions/1/llm-reply` → `{ "user_message": "Hello!" }`  
4. GET:-http://127.0.0.1:8000/session/{id}:-View messages → `/sessions/1`
---
### 🧩 Optional: Create `requirements.txt`

pip freeze > requirements.txt

