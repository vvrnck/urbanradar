import os
import json
from flask import Blueprint, request
from app.service import user_service
from app.util.decorators import authentication, requires_authz
from app.serializer.role import RolePatch, RoleDeletePatch, RoleList, RoleCreate, RoleGet

role_bp = Blueprint('role_api', __name__)


@role_bp.route("", methods=["GET"])
@authentication
def list_roles(**kwargs):
    json_return = json.loads(os.environ.get("JSON_RESPONSE"))
    tenant_id = kwargs.get("tenant_id")
    roles = user_service.list_roles(tenant_id)
    json_return["data"] = [RoleList.from_orm(role).dict() for role in roles]

    return json_return


@role_bp.route("/<role_id>", methods=["GET"])
@authentication
def get_role(role_id, **kwargs):
    json_return = json.loads(os.environ.get("JSON_RESPONSE"))
    tenant_id = kwargs.get("tenant_id")
    role = user_service.get_role_by_id(role_id, tenant_id)
    json_return["data"] = RoleGet.from_orm(role).dict()

    return json_return


@role_bp.route("", methods=['POST'])
@authentication
def role_create(**kwargs):
    json_return = json.loads(os.environ.get("JSON_RESPONSE"))
    data = request.get_json()
    role_data = RoleCreate(**data)
    role = user_service.create_role(role_data)
    json_return["data"] = RoleDeletePatch.from_orm(role).dict()

    return json_return


@role_bp.route('/<role_id>', methods=['DELETE'])
@authentication
def role_delete(role_id, **kwargs):
    json_return = json.loads(os.environ.get("JSON_RESPONSE"))
    tenant_id = kwargs.get("tenant_id")
    role = user_service.delete_role(role_id, tenant_id)
    json_return["data"] = RoleDeletePatch.from_orm(role).dict()

    return json_return


@role_bp.route("/<role_id>", methods=['PATCH'])
@authentication
def role_edit(role_id, **kwargs):
    json_return = json.loads(os.environ.get("JSON_RESPONSE"))
    data = request.get_json()
    role_patch = RolePatch(**data)
    role = user_service.edit_role(role_id, role_patch)
    json_return["data"] = RoleDeletePatch.from_orm(role).dict()

    return json_return
