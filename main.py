from fastapi import FastAPI
from config.database import check_db_connection, create_tables, engine
from controller import userController, authController
import asyncio
import model


app = FastAPI()

@app.on_event("startup")
async def startup():
    await check_db_connection()
    await create_tables()
    
@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()  
    
    
app.include_router(userController.router)
app.include_router(authController.router)

@app.get("/")
def root():
    return {"message": "Welcome to Library Management System"}


