#this file is for authentication of user signup and login
from fastapi import APIRouter,Depends,HTTPException,status
from schemas import UserSignup,UserLogin
from database import get_db
from databasemodels import User
from security import generate_token,hash_password,varify_password
authetication_router=APIRouter()
@authetication_router.post("/signup")
# @authentication_router.post("/signup")
def signup(request: UserSignup, db=Depends(get_db)):
    hashed_password = hash_password(request.password)
    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    new_user = User(username=request.username, email=request.email, password_hash=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  

    jwt_token = generate_token(new_user.user_id)  
    return {
        "status": "success code: 200",
        "message": "User created successfully",
        "token": jwt_token
    }


@authetication_router.post("/login")
def login(request:UserLogin,db=Depends(get_db)):
    user=db.query(User).filter(User.email==request.email).first()

    if user==None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="wrong password or email")
    does_password_match=varify_password(request.password,user.password_hash)
    if does_password_match==False:
       raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="wrong password or email")
    jwt_token=generate_token(user.user_id)
    return {"status":"Success","code":200,"Message":"login Sucessfull","token":jwt_token}

