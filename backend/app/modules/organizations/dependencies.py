from sqlalchemy.orm import Session
from fastapi import Depends

from app.database.session import get_db


def get_database() -> Session:
    return Depends(get_db)