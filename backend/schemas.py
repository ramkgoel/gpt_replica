from pydantic import BaseModel 
from typing import List

class ChatMsg(BaseModel):
    role: str
    content: str

class Chat(BaseModel):
    chat_id: str
    messages: List[ChatMsg]

# Why BaseModel?
#   Pydantic’s BaseModel offers data validation and serialization capabilities, 
#   making it well-suited for tasks like validating and parsing incoming data in web applications, 
#   as well as serializing data for API responses, ensuring that data adheres to the specified schema.