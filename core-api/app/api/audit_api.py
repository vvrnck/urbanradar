import os
import json
from flask import Blueprint, jsonify, request
from app.service.auditlog_service import AuditLogService
from app.util.decorators import authentication

audit_bp = Blueprint("audit_api", __name__)


@audit_bp.route("/<object_id>", methods=["GET"])
@authentication
def get_audit_for_object(object_id, **kwargs):
    object_type = request.args.get("type")
    json_response = json.loads(os.environ.get("JSON_RESPONSE"))
    audit_service = AuditLogService()
    audit_resp = audit_service.get_audit_by_type_and_id(object_id, object_type)
    json_response["data"] = audit_resp
    return jsonify(json_response)
