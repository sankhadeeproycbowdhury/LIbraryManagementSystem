from fastapi import FastAPI
from config.database import check_db_connection, create_tables, engine
from controller import userController, authController, studentController, bookController, bookIssueController
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from utils import check_and_send_reminders
import model


app = FastAPI()

scheduler = AsyncIOScheduler()

@app.on_event("startup")
async def startup():
    await check_db_connection()
    await create_tables()
    scheduler.add_job(check_and_send_reminders, "cron", hour=17, minute=00) 
    scheduler.start()
    
    
@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()  
    scheduler.shutdown()
    
    
app.include_router(userController.router)
app.include_router(authController.router)
app.include_router(studentController.router)
app.include_router(bookController.router)
app.include_router(bookIssueController.router)


@app.get("/")
def root():
    return {"message": "Welcome to Library Management System"}


