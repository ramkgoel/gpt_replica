from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "sqlite:///chat.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# https://medium.com/towards-data-engineering/fastapi-with-sql-1c7852ccbf21
# It 
# - defines a DATABASE_URL pointing to an SQLite database file, 
# - creates a database engine with additional configuration for SQLite thread safety, 
# - establishes a session factory with options to control transaction behavior, 
# - and sets up a base class for declarative database models.