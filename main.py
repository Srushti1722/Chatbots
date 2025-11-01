from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessionLocal, init_db, ChatSession, Message
from datetime import datetime
app = FastAPI(title="Chat Session API")
init_db()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
class CreateSessionRequest(BaseModel):
    user_name: str
class AddMessageRequest(BaseModel):
    sender: str
    text: str
class AIReplyRequest(BaseModel):
    user_message: str
@app.post("/sessions")
def create_session(req: CreateSessionRequest, db: Session = Depends(get_db)):
    new_session = ChatSession(user_name=req.user_name)
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return {"session_id": new_session.id, "user_name": new_session.user_name}
@app.post("/sessions/{session_id}/messages")
def add_message(session_id: int, req: AddMessageRequest, db: Session = Depends(get_db)):
    session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    msg = Message(session_id=session_id, sender=req.sender, text=req.text)
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return {"message_id": msg.id, "sender": msg.sender, "text": msg.text}
@app.get("/sessions/{session_id}")
def get_session_messages(session_id: int, db: Session = Depends(get_db)):
    session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    messages = (
        db.query(Message)
        .filter(Message.session_id == session_id)
        .order_by(Message.timestamp.asc())
        .all()
    )
    return {
        "session_id": session.id,
        "user_name": session.user_name,
        "messages": [
            {"sender": m.sender, "text": m.text, "timestamp": m.timestamp}
            for m in messages
        ],
    }
@app.post("/sessions/{session_id}/llm-reply")
def generate_llm_reply(session_id: int, req: AIReplyRequest, db: Session = Depends(get_db)):
    session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    ai_reply = f"AI Response to: {req.user_message}"
    bot_message = Message(session_id=session_id, sender="bot", text=ai_reply)
    db.add(bot_message)
    db.commit()
    db.refresh(bot_message)

    return {"bot_reply": ai_reply}
