from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.database import get_db

from .schema import UserBase

router = APIRouter(
    tags=["user"],
    prefix="/user",
)


@router.get("/", response_model=UserBase)
def read_user(db: Session = Depends(get_db)):
    return {
        "name": "John Doe",
        "email": "",
    }
