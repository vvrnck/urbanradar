from pydantic import BaseModel
from typing import Optional


class PropertiesData(BaseModel):
    image: Optional[str]
    icon: str

