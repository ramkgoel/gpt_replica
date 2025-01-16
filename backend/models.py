from sqlalchemy import Column, Integer, String, Text
from database import Base
import uuid 
import json 

from database import Base

def generate_uuid():
    return str(uuid.uuid4())

class ChatModel(Base):
    """
    A single table 'chats' that stores:
        - chat_id: unique UUID. 
        - messages: Text-encoded messages: ChatMsg[]. 
            e.g. [{"role": "user", "content": "Hello there!"}, {"role": "assistant", "content": "Hi! How can I help you today?"}]
    """
    # When we load from database, we use json.loads(chat.messages) to convert back to ChatMsg[] type. 

    __tablename__ = "chats" 

    chat_id = Column(String, primary_key=True, default=generate_uuid)
    messages = Column(Text, default="[]")





# Base class and its column definitions provide a structured blueprint for creating and interacting 
# with a table in the database using SQLAlchemy, specifying the data types and constraints for each column.

# Each member of db is ChatModel

# Note: 
# - ChatModel's messages is a Text field. (Model) 
# - Chat's messages is ChatMsg[]. (Schema)