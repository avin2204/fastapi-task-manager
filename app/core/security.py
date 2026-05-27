from passlib.context import CryptContext

from jose import JWTError, jwt

from datetime import datetime, timedelta, UTC

from fastapi import Depends, HTTPException, status

from fastapi.security import OAuth2PasswordBearer

from dotenv import load_dotenv

import os


# Load environment variables
load_dotenv()


# Environment Variables
SECRET_KEY = os.getenv("SECRET_KEY", "mysupersecretkey")

ALGORITHM = os.getenv("ALGORITHM", "HS256")

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)
)


# Password Hashing
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# OAuth2 Scheme
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)


# =========================
# HASH PASSWORD
# =========================

def hash_password(password: str):

    return pwd_context.hash(password)


# =========================
# VERIFY PASSWORD
# =========================

def verify_password(
    plain_password,
    hashed_password
):

    return pwd_context.verify(
        plain_password,
        hashed_password
    )


# =========================
# CREATE JWT TOKEN
# =========================

def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.now(UTC) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({
        "exp": expire
    })

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt


# =========================
# VERIFY JWT TOKEN
# =========================

def verify_access_token(
    token: str
):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        email = payload.get("sub")

        if email is None:

            return None

        return email

    except JWTError:

        return None


# =========================
# GET CURRENT USER
# =========================

def get_current_user(
    token: str = Depends(oauth2_scheme)
):

    email = verify_access_token(token)

    if email is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )

    return email