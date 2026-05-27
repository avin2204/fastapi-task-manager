from fastapi import FastAPI

from app.database import engine, Base
from app.models.user_model import User
from app.routers.user_router import router
from app.models.task_model import Task
from app.routers.task_router import router as task_router
#Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router)
app.include_router(task_router)

@app.get("/")
def home():
    return {
        "message": "TaskFlow Backend Running"
    }

