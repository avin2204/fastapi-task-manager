from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session

from app.database import get_db

from app.models.user_model import User

from app.schemas.user_schema import (
    UserCreate,
    UserLogin
)

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user
)

router = APIRouter()


# =========================
# REGISTER USER
# =========================

@router.post("/register")
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    # Check if email already exists
    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Hash password
    hashed_password = hash_password(
        user.password
    )

    # Create new user
    new_user = User(

        username=user.username,

        email=user.email,

        password=hashed_password,

        role=user.role
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return {
        "message": "User created successfully",
        "user_id": new_user.id,
        "role": new_user.role
    }


# =========================
# LOGIN USER
# =========================

@router.post("/login")
def login_user(
    user: UserLogin,
    db: Session = Depends(get_db)
):

    # Find user by email
    db_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not db_user:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid Email"
        )

    # Verify password
    password_check = verify_password(
        user.password,
        db_user.password
    )

    if not password_check:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Password"
        )

    # Create JWT token
    access_token = create_access_token(
        data={
            "sub": db_user.email,
            "role": db_user.role
        }
    )

    return {
        "message": "Login Successful",
        "access_token": access_token,
        "token_type": "bearer",
        "role": db_user.role
    }


# =========================
# USER PROFILE
# =========================

@router.get("/profile")
def get_profile(

    current_user: str = Depends(get_current_user)

):

    return {
        "message": "Protected Route Accessed",
        "current_user": current_user
    }


# =========================
# ADMIN ONLY ROUTE
# =========================

@router.get("/admin")
def admin_dashboard(

    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)

):

    db_user = db.query(User).filter(
        User.email == current_user
    ).first()

    if db_user.role != "admin":

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    return {
        "message": "Welcome Admin",
        "admin": db_user.email
    }