import os
import json
from flask import Blueprint, jsonify, request
from app.util.decorators import authentication
from app.service import user_service
from app.serializer.scope import Scope

scope_bp = Blueprint("scope_api", __name__)


@scope_bp.route("", methods=["GET"])
@authentication
def list_scopes(**kwargs):
    json_response = json.loads(os.environ.get("JSON_RESPONSE"))
    scopes = user_service.list_scopes()
    json_response["data"] = [Scope.from_orm(scope).dict() for scope in scopes]
    return jsonify(json_response)
