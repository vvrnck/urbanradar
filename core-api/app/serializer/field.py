from pydantic import BaseModel
from typing import List, Optional


class FieldConfigOption(BaseModel):
    key: str
    label: dict


class FieldConfigPost(BaseModel):
    key: str
    label: dict
    layer_id: int
    visible: bool
    order: int
    tenant_id: int
    field_config_options: List[FieldConfigOption]


class FieldConfigOptionResponse(BaseModel):
    id: int
    key: str
    label: dict

    class Config:
        orm_mode = True


class FieldConfigResponse(BaseModel):
    id: int
    key: str
    label: dict
    visible: bool
    tenant_id: int
    options: List[FieldConfigOptionResponse]

    class Config:
        orm_mode = True


class FieldData(BaseModel):
    key: str
    value: Optional[str]
    field_config_id: str
    value: str
    extra_props: Optional[str]

    class Config:
        orm_mode = True


class FieldResponse(BaseModel):
    id: int
    key: str
    field_config_id: int
    value: str
    extra_props: Optional[str]

    class Config:
        orm_mode = True

