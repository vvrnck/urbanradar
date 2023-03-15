from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from pydantic import Field


class Scope(BaseModel):
    id: int
    name: Optional[str]

    class Config:
        orm_mode = True
