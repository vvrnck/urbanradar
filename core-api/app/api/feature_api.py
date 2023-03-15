import os
import json
from flask import Blueprint, jsonify, request, g
from app.serializer.feature import (
    FeaturePost,
    FeaturePatch,
    FeatureResponse,
    FeatureClick,
)
from app.service.feature_service import FeatureService
from app.util.decorators import authentication, audit, requires_authz

feature_bp = Blueprint("feature_api", __name__)


# Create : Receberá Nome, Tipo, Properties (a definir - pensar em deixar genérico) e geometry.
# Depois criará feature e properties de acordo.
@feature_bp.route("", methods=["POST"])
@authentication
@audit
def feature_create(**kwargs):
    json_return = json.loads(os.environ.get("JSON_RESPONSE"))
    data = request.get_json()
    feat_data = FeaturePost.parse_obj(data)
    feature_service = FeatureService()
    feature = feature_service.create_feature_new(feat_data)
    resp = FeatureResponse.from_orm(feature)
    json_return["data"] = resp.dict()

    g.audit_data.update({
        'object_type': 'Feature',
        'object_id': resp.id,
        'action': 'CREATE',
    })

    return json_return


@feature_bp.route("/<feature_id>", methods=["DELETE"])
@authentication
@audit
def feature_delete(feature_id, **kwargs):
    json_return = json.loads(os.environ.get("JSON_RESPONSE"))
    tenant_id = kwargs.get("tenant_id")
    feature_service = FeatureService()
    confirmation = feature_service.delete_feature_by_id(
        feature_id, tenant_id
    )

    g.audit_data.update({
        'object_type': 'Feature',
        'object_id': confirmation.id,
        'action': 'DELETE',
    })

    return json_return


@feature_bp.route("/<feature_id>", methods=["PATCH"])
@authentication
@audit
def update_feature(feature_id, **kwargs):
    json_return = json.loads(os.environ.get("JSON_RESPONSE"))
    data = request.get_json()
    feat_data = FeaturePatch(**data)
    feature_service = FeatureService()
    feature = feature_service.update_feature_by_id(feature_id, feat_data)
    resp = FeatureResponse.from_orm(feature)
    json_return["data"] = resp.dict()

    g.audit_data.update({
        'object_type': 'Feature',
        'object_id': resp.id,
        'action': 'UPDATE',
    })

    return json_return


@feature_bp.route("/<feature_id>/chart", methods=["GET"])
@authentication
def feature_click(feature_id, **kwargs):
    json_return = json.loads(os.environ.get("JSON_RESPONSE"))
    data = {**request.args}
    if 'fields' in data.keys():
        data["fields"] = data["fields"].split("|")
    feat_data = FeatureClick(**data)
    feature_service = FeatureService()
    confirmation = feature_service.get_chart_by_feature(feature_id, feat_data, int(kwargs['tenant_id']))
    json_return["data"] = confirmation

    return jsonify(json_return)


