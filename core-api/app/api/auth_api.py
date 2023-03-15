import os
import json
from flask import Blueprint, jsonify, request
from app.service import auth_service
from app.service.management_service import ManagementService
from app.util.decorators import authentication_tenantless

auth_bp = Blueprint('auth_api', __name__)


#Adicionar Feature Collections e Tokens viram padrao com .
@auth_bp.route('/token', methods=['POST'])
def login_tenantless():
    json_return = json.loads(os.environ.get("JSON_RESPONSE"))
    access_token = request.json.get("access_token")
    user_info = auth_service.get_user_info_from_firebase(access_token)
    uid = user_info.get("uid")
    tenant_list, user = auth_service.get_user_tenants(uid)
    print(user)
    token = auth_service.generate_user_token_tenantless(user.id, uid, user.email, user.name, user.active)
    user_resp = {
        "active": user.active,
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "tenants": tenant_list,
        "token": token
    }
    json_return["data"] = user_resp

    return jsonify(json_return)


@auth_bp.route('/tenant/<tenant_id>/token', methods=['POST'])
@authentication_tenantless
def login_with_tenant(tenant_id: int, **kwargs):
    json_return = json.loads(os.environ.get("JSON_RESPONSE"))
    user_id = kwargs.get("user_id")
    email = kwargs.get("email")
    uid = kwargs.get("uid")
    active = kwargs.get("active")
    name = kwargs.get("name")
    scopes, roles = auth_service.get_user_scopes(user_id, tenant_id)
    feature_collections = auth_service.get_feature_collections_by_tenant(tenant_id)
    token = auth_service.generate_user_token(user_id, uid, email, tenant_id, roles, scopes, feature_collections, name)
    user = {
        "id": user_id,
        "token": token,
        "email": email,
        "name": name,
        "active": active
    }
    json_return["data"] = user

    return jsonify(json_return)
