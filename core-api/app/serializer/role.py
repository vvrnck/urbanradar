from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from pydantic import Field
from app.serializer.scope import Scope


class RolePatch(BaseModel):
    tenant_id: int
    scopes: Optional[List[Scope]] = []
    name: Optional[str]


class RoleList(BaseModel):
    id: int
    tenant_id: Optional[int]
    name: str

    class Config:
        orm_mode = True


class RoleDeletePatch(BaseModel):
    id: int
    tenant_id: Optional[int]
    name: str
    default: bool
    scopes: List[Scope] = Field(alias="scopes_entity")
    last_update: datetime
    creation_date: datetime

    class Config:
        orm_mode = True


class RoleGet(BaseModel):
    id: int
    tenant_id: Optional[int]
    name: str
    default: bool
    scopes: List[Scope] = Field(alias="scopes_entity")
    users: 'List[UserList]'
    last_update: datetime
    creation_date: datetime

    class Config:
        orm_mode = True


class RoleCreate(BaseModel):
    tenant_id: int
    name: str
    scopes: List[Scope] = []

    class Config:
        orm_mode = True


from app.serializer.user import UserList
RoleGet.update_forward_refs()
