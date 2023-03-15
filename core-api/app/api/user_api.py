import os
import json
from flask import Blueprint, request
from app.service import user_service
from app.util.decorators import authentication, requires_authz
from app.serializer.user import UserList, UserPatch, UserGet, UserCreate
from app.serializer.role import RoleList

user_bp = Blueprint('user_api', __name__)


@user_bp.route("", methods=["GET"])
@authentication
def list_users(**kwargs):
    json_return = json.loads(os.environ.get("JSON_RESPONSE"))
    tenant_id = kwargs.get("tenant_id")
    users = user_service.list_users(tenant_id)
    json_return["data"] = [UserList.from_orm(user).dict() for user in users]

    return json_return


@user_bp.route("/<id_>", methods=["GET"])
@authentication
def get_user(id_, **kwargs):
    json_return = json.loads(os.environ.get("JSON_RESPONSE"))
    tenant_id = kwargs.get("tenant_id")
    user, roles = user_service.get_user_by_id_with_roles(id_, tenant_id)
    json_return["data"] = {**UserGet.from_orm(user).dict(), "roles": [RoleList.from_orm(role).dict() for role in roles]}

    return json_return


@user_bp.route("", methods=['POST'])
@authentication
def create_user(**kwargs):
    json_return = json.loads(os.environ.get("JSON_RESPONSE"))
    data = request.get_json()
    user_data = UserCreate(**data)
    user, roles = user_service.create_user(user_data)
    json_return["data"] = {**UserGet.from_orm(user).dict(), "roles": [role.dict() for role in roles]}

    return json_return


@user_bp.route('/<id_>', methods=['DELETE'])
@authentication
def delete_user(id_, **kwargs):
    json_return = json.loads(os.environ.get("JSON_RESPONSE"))
    tenant_id = kwargs.get("tenant_id")
    user = user_service.delete_user_by_id(id_, tenant_id)
    json_return["data"] = UserGet.from_orm(user).dict()

    return json_return


@user_bp.route("/<id_>", methods=['PATCH'])
@authentication
def edit_user(id_, **kwargs):
    json_return = json.loads(os.environ.get("JSON_RESPONSE"))
    data = request.get_json()
    user_patch = UserPatch(**data)
    user = user_service.edit_user(id_, user_patch)
    json_return["data"] = UserGet.from_orm(user).dict()

    return json_return
