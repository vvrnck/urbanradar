import os
import json
from flask import Blueprint, jsonify, request
from app.serializer.field import FieldConfigPost, FieldConfigResponse
from app.service import field_service
from app.util.decorators import authentication

field_bp = Blueprint('field_api', __name__)


@field_bp.route("/config", methods=["POST"])
@authentication
def create_filter(**kwargs):
    json_response = json.loads(os.environ.get("JSON_RESPONSE"))
    fc_data = FieldConfigPost(**request.get_json())
    fc = field_service.create_field_config(fc_data)
    fc_resp = FieldConfigResponse.from_orm(fc)
    json_response["data"].append(fc_resp.dict())
    return jsonify(json_response)
