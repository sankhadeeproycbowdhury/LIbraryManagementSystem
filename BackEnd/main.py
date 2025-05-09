from fastapi import FastAPI
from config.database import check_db_connection, create_tables, engine
from controller import userController, authController, studentController, bookController, bookIssueController, adminController
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from utils import check_and_send_reminders, check_and_set_flag, check_or_create_admin
from fastapi.middleware.cors import CORSMiddleware
import model

app = FastAPI()

# Allowed Origins
origins = [
    "http://localhost:3000",  # If frontend is running on React or Vue
    "http://127.0.0.1:3000",
    "https://yourfrontenddomain.com"  # Add your production frontend domain
]

# Enable CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allowed frontend origins
    allow_credentials=True,  # Allow sending cookies
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

scheduler = AsyncIOScheduler()

@app.on_event("startup")
async def startup():
    await check_db_connection()
    await create_tables()
    await check_or_create_admin()
    scheduler.add_job(check_and_send_reminders, "cron", hour=12, minute=00) 
    scheduler.add_job(check_and_set_flag, "cron", hour=9, minute=45)
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
app.include_router(adminController.router)


@app.get("/")
def root():
    return {"message": "Welcome to Library Management System"}


