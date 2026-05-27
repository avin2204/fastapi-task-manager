from pydantic import BaseModel

from datetime import datetime


class TaskCreate(BaseModel):

    title: str

    description: str

    priority: str = "medium"


class TaskUpdate(BaseModel):

    title: str

    description: str

    status: str

    priority: str 


class TaskResponse(BaseModel):

    id: int

    title: str

    description: str | None

    status: str

    user_id: int

    priority: str

    class Config:

        from_attributes = True