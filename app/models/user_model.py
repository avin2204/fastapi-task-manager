from sqlalchemy import Column, Integer, String

from app.database import Base


class User(Base):

    __tablename__ = "users"

    # =========================
    # PRIMARY KEY
    # =========================

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # =========================
    # USERNAME
    # =========================

    username = Column(
        String,
        unique=True,
        nullable=False
    )

    # =========================
    # EMAIL
    # =========================

    email = Column(
        String,
        unique=True,
        nullable=False
    )

    # =========================
    # HASHED PASSWORD
    # =========================

    password = Column(
        String(255),
        nullable=False
    )

    # =========================
    # USER ROLE
    # =========================

    role = Column(
        String,
        default="user"
    )