from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

import os
load_dotenv()  # Load environment variables from .env file
SQLALCHEMY_DATABASE_URL = os.getenv("Database_URL")
#establish conn

engine = create_engine(SQLALCHEMY_DATABASE_URL)
#crete session object
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

    