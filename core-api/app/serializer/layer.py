from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class LayerPost(BaseModel):
    tenant: str
    name: str
    id_section: int
    selected: bool
    order: int
    active: bool
    style: dict
    editable: bool
    configurable: bool
    label: dict


class LayerResponse(BaseModel):
    id: int
    tenant: str
    name: str
    id_section: int
    selected: bool
    order: int
    active: bool = Field(default=None)
    style: dict
    editable: bool
    label: dict
    configurable: bool
    creation_date: Optional[datetime]
    last_update: Optional[datetime]

    class Config:
        orm_mode = True
