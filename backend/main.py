from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
import json
from typing import List

from models import ChatModel
from schemas import ChatMsg, Chat
from database import engine, SessionLocal, Base


Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def llm_pipeline(messages: List[ChatMsg]) -> ChatMsg:
    return ChatMsg(role="assistant", content="Hello!")

@app.get("/")
def home():
    return {"message": "Hello World"}

@app.post("/create_chat", response_model=Chat)
def create_chat(db: Session = Depends(get_db)):
    """
    Create a new chat. Default creates a chat_id and messages=[]. Add it to the database.
    Return the chat object.
    """
    chat = ChatModel() # Default creates a chat_id and messages=[].
    db.add(chat)
    db.commit()
    db.refresh(chat) 
    return Chat(chat_id=chat.chat_id, messages=[])

@app.get("/get_chat/{chat_id}", response_model=Chat) # Can also ommit /{chat_id} if we want to use the path parameter directly. But since chat_id is identifying a specific resource, it's better to use it.
def get_chat(chat_id: str, db: Session = Depends(get_db)):
    """
    Get a chat by chat_id. 
    Returns Chat object (chat_id, messages). Could choose to just output messages, but might as well do this. 
    Note: 
        - ChatModel's messages is a Text field. (Model) 
        - Chat's messages is ChatMsg[]. (Schema)
    """
    chatModel = db.query(ChatModel).filter(ChatModel.chat_id == chat_id).first() # Each entry of db is type ChatModel.
    if not chatModel:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    messages = json.loads(chatModel.messages) # Convert from Text to ChatMsg[].
    return Chat(chat_id=chatModel.chat_id, messages=messages)

@app.post("/continue_chat/{chat_id}", response_model=ChatMsg)
def continue_chat(chat_id: str, new_message: ChatMsg, db: Session = Depends(get_db)):
    """
    Continue a chat by chat_id. 
        1. Add new_message to messages in db for chat_id. 
        2. Inputs updated messages: ChatMsg[] into LLM, prompted to respond to last message.
        3. Returns answer as ChatMsg, and adds it to messages in db for chat_id.
    """

    # 1. Add new_message to messages in db for chat_id. 
    chatModelRow = db.query(ChatModel).filter(ChatModel.chat_id == chat_id).first() # The ChatModel in db for chat_id.
    if not chatModelRow:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    messages = json.loads(chatModelRow.messages) # Convert from Text to ChatMsg[].
    messages.append({"role": new_message.role, "content": new_message.content})
    chatModelRow.messages = json.dumps(messages)
    db.commit()
    db.refresh(chatModelRow)

    # return db.query(ChatModel).filter(ChatModel.chat_id == chat_id).first()

    # 2. Inputs updated messages: ChatMsg[] into LLM, prompted to respond to last message.
    llm_response = llm_pipeline(messages)
    
    # 3. Returns answer as ChatMsg, and adds it to messages in db for chat_id.
    messages.append({"role": llm_response.role, "content": llm_response.content})
    chatModelRow.messages = json.dumps(messages)
    db.commit()
    db.refresh(chatModelRow)

    return ChatMsg(role=llm_response.role, content=llm_response.content)
