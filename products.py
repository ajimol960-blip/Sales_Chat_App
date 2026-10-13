from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from security import get_current_user
from database import get_db
from databasemodels import Product
from schemas import CreateProduct
from datetime import datetime
product_router = APIRouter()

@product_router.get("/products")
async def get_all_product(current_user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
   prducts = db.query(Product).all()
   return {"products": prducts}

@product_router.post("/products")
async def create_product(product: CreateProduct, current_user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
   new_product = Product(
       title=product.title,
       category=product.category,
       description=product.description,
       price=product.price,
       current_stock=product.current_stock,
       created_at=datetime.utcnow()
   )
   db.add(new_product)
   db.commit()
   db.refresh(new_product)
   return {"product": new_product}