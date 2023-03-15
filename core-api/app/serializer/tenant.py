from pydantic import BaseModel, Field
from datetime import datetime


class TenantPost(BaseModel):
    name: str
    city: str
    city_code: str
    country: str
    status: int = Field(1, const=True)


class TenantResponse(BaseModel):
    id: int
    name: str
    city: str
    city_code: str
    country: str
    status: int
    creation_date: datetime
    last_update: datetime

    class Config:
        orm_mode = True
        use_enum_values = True


class TenantResponseList(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
