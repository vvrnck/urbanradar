import os
import json
from flask import Blueprint, jsonify, request
from app.serializer.section import SectionPost, SectionResponse
from app.service import section_service
from app.util.decorators import authentication

section_bp = Blueprint('section_api', __name__)


@section_bp.route("", methods=["POST"])
@authentication
def create_section(**kwargs):
    json_response = json.loads(os.environ.get("JSON_RESPONSE"))
    section_data = SectionPost.parse_obj(request.get_json())
    section = section_service.create_section(section_data)
    section_resp = SectionResponse.from_orm(section)
    json_response["data"].append(section_resp.dict())
    return jsonify(json_response)


@section_bp.route("", methods=["GET"])
@authentication
def list_section(**kwargs):
    json_response = json.loads(os.environ.get("JSON_RESPONSE"))
    tenant_id = kwargs.get("tenant_id")
    section_list = section_service.list_sections(tenant_id)
    json_response["data"].extend(section_list)
    return jsonify(json_response)


@section_bp.route("/<section_id>", methods=["GET"])
@authentication
def get_section(section_id, **kwargs):
    json_response = json.loads(os.environ.get("JSON_RESPONSE"))
    tenant_id = kwargs.get("tenant_id")
    section = section_service.get_section_by_id(section_id, tenant_id)
    sec_resp = SectionResponse.from_orm(section)
    json_response["data"] = sec_resp.dict()
    return jsonify(json_response)


@section_bp.route("/<section_id>", methods=["PATCH"])
@authentication
def update_section(section_id, **kwargs):
    json_response = json.loads(os.environ.get("JSON_RESPONSE"))
    tenant_id = kwargs.get("tenant_id")
    section_data = SectionPost.parse_obj(request.get_json())
    section = section_service.update_section_by_id(section_id, tenant_id, section_data)
    sec_resp = SectionResponse.from_orm(section)
    json_response["data"] = sec_resp.dict()
    return jsonify(json_response)


@section_bp.route("/<section_id>", methods=["DELETE"])
@authentication
def delete_section(section_id, **kwargs):
    json_response = json.loads(os.environ.get("JSON_RESPONSE"))
    tenant_id = kwargs.get("tenant_id")
    section_service.delete_section_by_id(section_id, tenant_id)
    return jsonify(json_response)
