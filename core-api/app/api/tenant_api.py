import os
import json
from flask import Blueprint, jsonify, request
from app.util.decorators import authentication
from app.serializer.tenant import TenantPost, TenantResponse, TenantResponseList
from app.service import tenant_service

tenant_bp = Blueprint('tenant_api', __name__)


@tenant_bp.route("", methods=["POST"])
@authentication
def create_tenant(**kwargs):
    json_response = json.loads(os.environ.get("JSON_RESPONSE"))
    tenant_data = TenantPost.parse_obj(request.get_json())
    tenant = tenant_service.create_tenant(tenant_data)
    tenant_resp = TenantResponse.from_orm(tenant)
    json_response["data"] = tenant_resp.dict()
    return jsonify(json_response)


@tenant_bp.route("", methods=["GET"])
@authentication
def list_tenant(**kwargs):
    json_response = json.loads(os.environ.get("JSON_RESPONSE"))
    tenant_list = tenant_service.list_tenant()
    resp = [TenantResponseList.from_orm(tenant).dict() for tenant in tenant_list]
    json_response["data"] = resp
    return jsonify(json_response)


@tenant_bp.route("/<tenant_id>", methods=["GET"])
@authentication
def get_tenant(tenant_id, **kwargs):
    json_response = json.loads(os.environ.get("JSON_RESPONSE"))
    tenant = tenant_service.get_tenant_by_id(tenant_id)
    tenant_resp = TenantResponse.from_orm(tenant)
    json_response["data"] = tenant_resp.dict()
    return jsonify(json_response)


@tenant_bp.route("<tenant_id>", methods=["DELETE"])
@authentication
def delete_tenant(tenant_id, **kwargs):
    json_response = json.loads(os.environ.get("JSON_RESPONSE"))
    tenant_service.delete_tenant_by_id(tenant_id)
    return jsonify(json_response)
