from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    email: str
    degree: Optional[str]
