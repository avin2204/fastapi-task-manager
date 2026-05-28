from pydantic import BaseModel, EmailStr


# =========================
# USER REGISTRATION SCHEMA
# =========================

class UserCreate(BaseModel):

    username: str

    email: EmailStr

    password: str

    role: str = "user"


# =========================
# USER LOGIN SCHEMA
# =========================

class UserLogin(BaseModel):

    email: EmailStr

    password: str


# =========================
# USER RESPONSE SCHEMA
# =========================

class UserResponse(BaseModel):

    id: int

    username: str

    email: EmailStr

    role: str

    class Config:

        from_attributes = True