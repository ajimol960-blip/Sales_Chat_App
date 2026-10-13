from fastapi import APIRouter,Depends,HTTPException,status
from security import get_current_user

my_orders_routers=APIRouter()

@my_orders_routers.get("/my_orders")
def get_orders(current_user_id:int=Depends(get_current_user)):
    return {"message":"my orders","current_user_id":current_user_id}