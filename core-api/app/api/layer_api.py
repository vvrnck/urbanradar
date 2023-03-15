import os
import json
from flask import Blueprint, jsonify, request
from app.serializer.layer import LayerPost, LayerResponse
from app.serializer.feature import FeatureListMap
from app.service.layer_service import LayerService
from app.service.feature_service import FeatureService
from app.util.decorators import authentication

layer_bp = Blueprint("layer_api", __name__)


@layer_bp.route("", methods=["POST"])
@authentication
def create_layer(**kwargs):
    json_response = json.loads(os.environ.get("JSON_RESPONSE"))
    layer_data = LayerPost.parse_obj(request.get_json())
    layer_service = LayerService()
    layer = layer_service.create_layer(layer_data)
    layer_resp = LayerResponse.from_orm(layer)
    json_response["data"].append(layer_resp.dict())
    return jsonify(json_response)


@layer_bp.route("/<layer_id>", methods=["GET"])
@authentication
def get_layer(layer_id, **kwargs):
    json_response = json.loads(os.environ.get("JSON_RESPONSE"))
    tenant_id = kwargs.get("tenant_id")
    layer_service = LayerService()
    layer = layer_service.get_layer_by_id(layer_id, tenant_id)
    layer_resp = LayerResponse.from_orm(layer)
    json_response["data"] = layer_resp.dict()
    return jsonify(json_response)


@layer_bp.route("/<layer_id>", methods=["DELETE"])
@authentication
def delete_layer(layer_id, **kwargs):
    json_response = json.loads(os.environ.get("JSON_RESPONSE"))
    tenant_id = kwargs.get("tenant_id")
    layer_service = LayerService()
    layer_service.delete_layer_by_id(layer_id, tenant_id)
    return jsonify(json_response)


@layer_bp.route("/<layer_id>", methods=["PATCH"])
@authentication
def update_layer(layer_id, **kwargs):
    json_response = json.loads(os.environ.get("JSON_RESPONSE"))
    layer_data = LayerPost.parse_obj(request.get_json())
    tenant_id = kwargs.get("tenant_id")
    layer_service = LayerService()
    layer = layer_service.update_layer_by_id(layer_id, tenant_id, layer_data)
    layer_resp = LayerResponse.from_orm(layer)
    json_response["data"].append(layer_resp.dict())
    return jsonify(json_response)


@layer_bp.route("/<layer_id>/feature", methods=["GET"])
@authentication
def feature_list(**kwargs):
    json_return = json.loads(os.environ.get("JSON_RESPONSE"))
    data = {**request.args, "filters": request.args.getlist("filter[]"), "tenant": kwargs.get("tenant_id"), "id_layer": kwargs.get("layer_id")}
    feature_list_data = FeatureListMap(**data)
    feature_service = FeatureService()
    feats = feature_service.fetch_features_from_layer_between_dates(**feature_list_data.dict())
    json_return['data'] = feats
    return json_return


@layer_bp.route("", methods=["GET"])
@authentication
def list_layer(**kwargs):
    json_return = json.loads(os.environ.get("JSON_RESPONSE"))
    tenant = kwargs.get("tenant_id")
    layers = LayerService.list_layer(tenant)
    json_return['data'] = layers
    return json_return
