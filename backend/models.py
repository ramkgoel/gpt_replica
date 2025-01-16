from sqlalchemy import Column, Integer, String, Text
from database import Base
import uuid 
import json 

from database import Base

def generate_uuid():
    return str(uuid.uuid4())

class Chat(Base):
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




# https://medium.com/towards-data-engineering/fastapi-with-sql-1c7852ccbf21
# In above code snippet, a SQLAlchemy database model class called 
# User is defined, inheriting from the Base class, which was imported from a module named database we defined before. 
# This class represents a database table named “users.” 
# It contains four columns: id, name, email, and nickname. 
# The id column is defined as an integer and serves as the primary key for the table, ensuring each row has a unique identifier. 
# The other columns, name, email, and nickname, are defined as string fields. 
# This class and its column definitions provide a structured blueprint for creating and interacting 
# with a “users” table in the database using SQLAlchemy, specifying the data types and constraints for each column.