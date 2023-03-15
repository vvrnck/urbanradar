from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
from app.serializer.layer import LayerResponse


class SectionPost(BaseModel):
    tenant: str
    name: str
    icon: str
    order: int
    label: dict


class SectionResponse(BaseModel):
    id: int
    tenant: str
    name: str
    icon: str
    order: int
    label: dict
    layers: Optional[List[LayerResponse]]
    creation_date: datetime
    last_update: datetime

    class Config:
        orm_mode = True


class SectionResponseList(BaseModel):
    id: int
    tenant: str
    icon: str
    name: str
    label: dict

    class Config:
        orm_mode = True
