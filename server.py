from fastapi import FastAPI
from uuid import uuid4  
from typing import List, Literal

app = FastAPI()

class ChatMsg:
    """
    {role: "user" | "assistant", content: str}
    """
    role: Literal["user", "assistant"]
    content: str

class ChatMsgs:
    """
    List[ChatMsg]
    """
    msgs: List[ChatMsg]


@app.get("/create_chat")
def create_chat():
    """
    Create a new chat and return the chat_id
    And create entry in the database with the chat_id and empty ChatMsgs instance
    """
    chat_id = str(uuid4())
    # db.insert(chat_id, ChatMsgs())
    return {"chat_id": chat_id}


@app.get("/continue_chat")
def continue_chat(chat_id: str, ):
    return {"message": "Hello Worlddd", "item_id": item_id}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)