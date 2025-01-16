from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from models import Base, User
from schemas import UserSchema
from database import engine, SessionLocal

# Create all tables in the database (only needed once, or each time you modify models)
Base.metadata.create_all(bind=engine)

# Initialize FastAPI
app = FastAPI()

# Dependency to get a new database session for each request
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@app.get("/")
async def home():
    return {"message": "Hello, World!"}

@app.post("/adduser")
async def add_user(request: UserSchema, db: Session = Depends(get_db)):
    # Create a new User instance based on the incoming request
    user = User(
        name=request.name,
        email=request.email,
        nickname=request.nickname
    )
    db.add(user)
    db.commit()       # Commit the transaction
    db.refresh(user)  # Refresh to load any updates (e.g., generated IDs)
    return user

@app.get("/user/{user_name}")
async def get_user(user_name: str, db: Session = Depends(get_db)):
    # Query the database for the first user whose name matches user_name
    user = db.query(User).filter(User.name == user_name).first()
    if not user:
        raise HTTPException(
            status_code=404, 
            detail=f"User '{user_name}' not found"
        )
    return user
