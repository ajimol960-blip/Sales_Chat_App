from fastapi import FastAPI, WebSocket
from authentication import authetication_router
from products import product_router
from fastapi.middleware.cors import CORSMiddleware
from my_orders import my_orders_routers
from websocket_service import handle_chat_websocket
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
app=FastAPI()
app.add_middleware(CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(authetication_router)
app.include_router(my_orders_routers)
app.include_router(product_router)
# app.mount("/static", StaticFiles(directory="frontend/js"), name="js")
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
async def root():
    return FileResponse("frontend/login.html")
@app.get("/signup")
async def signup():
    return FileResponse("frontend/signup.html")
@app.get("/chat")
async def chat():   
    return FileResponse("frontend/chat.html")
@app.get("/login")
async def login():  
    return FileResponse("frontend/login.html")
# @app.get("/home")
# async def home():
#     return {"Message": "Welcome"}

@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket,token:str):
    await handle_chat_websocket(websocket,token)
    

