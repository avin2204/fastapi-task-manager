from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserLogin

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user
)

router = APIRouter()


@router.post("/register")
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    hashed_password = hash_password(
        user.password
    )

    new_user = User(

        username=user.username,
        email=user.email,
        password=hashed_password
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return {
        "message": "User created successfully",
        "user_id": new_user.id
    }


@router.post("/login")
def login_user(
    user: UserLogin,
    db: Session = Depends(get_db)
):

    db_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not db_user:

        return {
            "message": "Invalid Email"
        }

    password_check = verify_password(
        user.password,
        db_user.password
    )

    if not password_check:

        return {
            "message": "Invalid Password"
        }

    access_token = create_access_token(
        data={
            "sub": db_user.email
        }
    )

    return {
        "message": "Login Successful",
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get("/profile")
def get_profile(
    current_user: str = Depends(get_current_user)
):

    return {
        "message": "Protected Route Accessed",
        "current_user": current_user
    }