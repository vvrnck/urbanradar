from app.serializer.tenant import TenantPost
from app.util.exceptions import EntityNotFound
from app.model.Tenant import Tenant
from typing import List
from ext import db


def create_tenant(tenant_model: TenantPost) -> Tenant:
    tenant = Tenant(**tenant_model.dict())
    db.session.add(tenant)
    db.session.commit()
    return tenant


def list_tenant() -> List[Tenant]:
    tenant_list = db.session.query(Tenant).all()
    return tenant_list


def get_tenant_by_id(tenant_id: int) -> Tenant:
    tenant = db.session.query(Tenant).filter(Tenant.id == tenant_id).first()
    if not tenant:
        raise EntityNotFound
    return tenant


def delete_tenant_by_id(tenant_id: int) -> bool:
    db.session.query(Tenant).filter(Tenant.id == tenant_id).delete()
    return True
