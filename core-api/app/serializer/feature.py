from pydantic import BaseModel, Field, validator
from app.serializer.field import FieldData, FieldResponse
from app.serializer.properties import PropertiesData
from datetime import date
import json
from typing import List, Optional


class FeaturePost(BaseModel):
    type: str
    properties: Optional[dict]
    geometry: str
    layer_id: str
    properties: PropertiesData
    feature_collection_id: str
    tenant_id: int
    language: str
    fields: Optional[List[FieldData]]

    @validator('geometry', pre=True, whole=True)
    def geometry_to_str(cls, v):
        return json.dumps(v)


class FeaturePatch(BaseModel):
    geometry: Optional[str]
    fields: List[FieldData]
    tenant_id: int
    language: str = "pt"

    @validator('geometry', pre=True, whole=True)
    def geometry_to_str(cls, v):
        return json.dumps(v)


class FeatureResponse(BaseModel):
    id: int
    type: str
    geometry: list
    layer_id: str
    tenant_id: int
    fields: List[FieldResponse]

    @validator('geometry', pre=True, whole=True)
    def geometry_to_json(cls, v):
        return json.loads(v)

    class Config:
        orm_mode = True


class FeatureClick(BaseModel):
    id_layer: str
    dt_start: date
    dt_end: date


class FeatureListMap(BaseModel):
    filters: dict
    tenant: int
    id_layer: int
    dt_start: date
    dt_end: date

    @validator('filters', pre=True, whole=True)
    def filters_to_dict(cls, v):
        resp = {}
        for f in v:
            val = f.split("|")
            if val[0] not in resp:
                resp[val[0]] = [val[1]]
            else:
                resp[val[0]].append(val[1])
        return resp
