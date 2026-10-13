# create orm base( define model class)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime


from database import engine
from sqlalchemy import Column, Integer, String, ForeignKey

Base = declarative_base()

#Define the Model:

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True,index=True)
    username = Column(String,index=True)
    email=Column(String,unique=True,index=True)
    password_hash=Column(String)
    chathistory=relationship("chathistory", back_populates="user")
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True,index=True)
    title = Column(String,index=True)
    category = Column(String,index=True)
    description = Column(String)
    price = Column(Integer)
    current_stock = Column(Integer)
    created_at = Column(String)

class chathistory(Base):
    __tablename__ = "chathistory"
    id = Column(Integer, primary_key=True,index=True)
     
    user_id = Column(Integer,ForeignKey("users.user_id"))
    sender = Column(String)
    message = Column(String)
    timestamp = Column(String)
    user=relationship("User", back_populates="chathistory")
Base.metadata.create_all(bind=engine)

