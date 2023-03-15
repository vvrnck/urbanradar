from pydantic import BaseModel, Field, validator
from app.serializer.field import FieldData, FieldResponse
from app.serializer.properties import PropertiesData
from datetime import date, datetime
import json
from typing import List, Optional


class AuditResponseList(BaseModel):
    object_id: int
    object_type: str
    user_id: int
    user_name: str
    action: str
    browser: str
    ip: str
    data: List[dict]
    tenant: int
    creation_date: datetime

    class Config:
        orm_mode = True
