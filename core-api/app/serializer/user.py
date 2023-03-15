from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from app.serializer.role import RoleList


class UserPatch(BaseModel):
    name: Optional[str]
    roles: Optional[List[RoleList]]
    email: Optional[str]
    tenant_id: int


class UserList(BaseModel):
    id: str
    name: str

    class Config:
        orm_mode = True


class UserGet(BaseModel):
    id: int
    uid: str
    name: str
    email: str
    last_update: datetime
    creation_date: datetime

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    tenant_id: int
    uid: str
    email: str
    name: str
    roles: List[RoleList]
    active: bool
