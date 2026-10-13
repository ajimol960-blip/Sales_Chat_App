from argon2 import PasswordHasher
from typing import Optional
from fastapi import Header,HTTPException,status
import jwt
ph=PasswordHasher()
SECRET_KEY="gghghhghgh"

def hash_password(password:str)->str:
    return ph.hash(password)

def varify_password(password:str,hashed_password:str)->bool:
    try:
        return ph.verify(hashed_password,password)
    except:
        return False
def generate_token(user_id:int)->str:
    payload={"user_id":user_id}
    return jwt.encode(payload,SECRET_KEY,algorithm="HS256")

def verify_token(token:str)->int:
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=["HS256"])
        return payload["user_id"]
    except:
        return None
    
def get_current_user(authorization:Optional[str]=Header(None))->int:
    if authorization is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not authenticated")
    if not authorization.startswith("Bearer"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Authenicated")
    scheme,token=authorization.split()
    if scheme.lower()!="bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Authenicated")
    current_user_id=verify_token(token)
    if current_user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")
    return current_user_id