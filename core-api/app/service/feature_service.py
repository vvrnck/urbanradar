import math
import sys

from app.model.Chart import Tab, Chart, ChartType, ChartTypeTabLayer
from app.model.Field import Field, FieldConfigOptions, FieldConfig
from app.model.Feature import Feature
from app.model.Layer import Layer
from app.model.Properties import Properties
from app.serializer.feature import FeaturePatch, FeaturePost
from app.model.Calendar import Calendar
from sqlalchemy.orm import aliased
from ext import db
from sqlalchemy import func, or_, and_
from flask import g
from typing import List
from app.util.exceptions import EntityNotFound
from app.serializer.feature import FeatureClick
import json
import copy


class FeatureService:
    @staticmethod
    def create_feature(type_, properties, geometry, layer_id, origin):
        # TODO Implementar name, type_, properties
        if type_ == "marker":
            lat = str(geometry["lat"])
            lng = str(geometry["lng"])
            code = lat + "_" + lng
            geo = "POINT Z (" + lat + " " + lng + " )"
            geo_txt = "[" + lat + ", " + lng + ", 0]"
            style = '{"marker": {"marker": true,"markerName": "pin-black.png"}}'

            # Recebe Group ID e String do Category
            feat = Feature(layer_id, origin, code, geo, geo_txt)
            feat.style = style

            db.session.add(feat)
            db.session.commit()

            for prop in properties:
                cat = properties[prop]
                new_cat = Field.query.filter(Field.id_group == int(prop)).filter(Field.name == cat).first()
                if not new_cat:
                    new_cat = Field(int(prop), origin, cat)
                    db.session.add(new_cat)
                    db.session.commit()

                prop = Properties(feat.id, origin, new_cat.id, 1)
                db.session.add(prop)
                db.session.commit()

        else:
            raise Exception("Only 'Marker' types implemented")

        success_json = {"id": feat.id, "prop_id": prop.id}
        return success_json

    @staticmethod
    def delete_feature_delete_properties(feature_id, layer_id, tenant_id):
        feat_to_delete = (
            Feature.query.filter(Feature.id == feature_id)
            .filter(Feature.layer_id == layer_id)
            .filter(Feature.tenant_id == tenant_id)
            .first()
        )

        props_to_delete = Properties.query.filter(Properties.feature_id == feature_id).all()

        for prop in props_to_delete:
            db.session.delete(prop)
        db.session.commit()

        db.session.delete(feat_to_delete)
        db.session.commit()

        return feat_to_delete

    @staticmethod
    def fetch_feature_and_properties(tenant, id_layer, code, dt_start, dt_end):
        feats = (
            Feature.query.join(Properties)
            .add_entity(Properties)
            .filter(
                Feature.code == code,
                Properties.tenant_id == tenant,
                Feature.layer_id == id_layer,
            )
            .filter(Properties.date.between(dt_start, dt_end))
            .all()
        )

        return feats

    @staticmethod
    def fetch_charts_from_feature(feature_code, id_layer, tenant, dt_start, dt_end):
        chart_queries = GenericQueries.query.filter(
            GenericQueries.tenant == tenant,
            GenericQueries.layers.astext == "[%]".format(id_layer),
        ).all()
        chart_queries = (
            db.session.query(
                GenericQueries.query_sql,
                GenericQueries.query_key,
                GenericQueries.filters,
                GenericQueries.layers,
            )
            .filter(GenericQueries.origin == origin)
            .filter(GenericQueries.type_ == "features")
            .all()
        )

    def fetch_features_from_layer_between_dates(self, tenant, id_layer, dt_start, dt_end, filters):
        calendar_availability = (
            db.session.query(Calendar.feature_id)
            .filter(Calendar.available_date.between(dt_start, dt_end))
            .filter(Calendar.layer_id == id_layer)
            .group_by(Calendar.feature_id)
            .subquery()
        )
        feats = (
            db.session.query(
                func.json_build_object(
                    "id",
                    Feature.id,
                    "geometry",
                    Feature.geometry,
                    "name",
                    Feature.code,
                    "type",
                    Feature.type,
                    "label",
                    Properties.label,
                    "style",
                    Properties.style,
                    "properties",
                    func.json_build_object("image", Properties.image, "id", Properties.id),
                    "fields",
                    func.array_agg(
                        func.json_build_object(
                            "id",
                            Field.id,
                            "key",
                            Field.key,
                            "value",
                            Field.value,
                            "extra_props",
                            Field.extra_props,
                            "field_config_id",
                            Field.field_config_id,
                        )
                    ),
                ).label("features"),
            )
            .join(Properties, Properties.feature_id == Feature.id)
            .filter(Feature.layer_id == id_layer)
            .filter(
                or_(
                    Feature.type == "MARKER",
                    Feature.id.in_(calendar_availability)
                )
            )
            .filter(Feature.tenant_id == tenant)
        )
        # Creating a subquery to filter the data
        if filters:
            field_filtered = db.session.query(Feature.id)
            for f in filters:
                alias_field = aliased(Field)
                alias_fc = aliased(FieldConfig)
                field_filtered = field_filtered.join(alias_field, alias_field.feature_id == Feature.id).join(alias_fc, alias_fc.id == alias_field.field_config_id).filter(and_(alias_fc.key == f, alias_field.key.in_(filters.get(f)), alias_field.date.between(dt_start, dt_end)))
            field_filtered = field_filtered.group_by(Feature.id).subquery()
            feats = feats.filter(Feature.id.in_(field_filtered))
        feats = feats.outerjoin(Field, and_(Field.feature_id == Feature.id, or_(Feature.type == "MARKER", Field.date.between(dt_start, dt_end)))).group_by(Feature.id, Properties.id).all()
        success_json = {"features": [], "items": {"polygon": [], "marker": [], "point": []}}
        item_arr = {"polygon": [], "point": []}
        has_marker = 0
        feat_none = False

        feat_point_color = {}

        layer_resp = db.session.query(Layer.style).filter(Layer.id == id_layer).first()
        layer_style = layer_resp.style
        color_scale = layer_style.get("colorScale")
        color_point = color_scale.get("point")

        point_color_list = []

        for feat_data in feats:
            has_value = 0
            feat = feat_data.features
            feat_type = feat.get("type").lower()
            if feat_type == "marker":
                has_marker = 1
            total_value = 0
            feat["fields"] = sorted(feat["fields"], key=lambda x: x.get("value"), reverse=True)
            for field in feat.get("fields"):
                if field.get("id") is not None:
                    field_key = field.get("key")
                    if field_key in color_point and feat_type == "point":
                        feat_point_color[feat.get("id")] = field_key
                        if field_key not in point_color_list:
                            point_color_list.append(field_key)
                    total_value += float(field.get("value"))
                    has_value = 1
            if not has_value:
                feat["fields"] = []
                if feat_type == "polygon":
                    feat["total_value"] = 0
                    feat_none = True
            elif feat_type != "marker" and feat_type != "image_overlay":
                item_arr[feat_type].append(total_value)
                feat["total_value"] = total_value
            style = json.loads(feat.get("style"))
            feat["style"] = style
            feat["geometry"] = json.loads(feat.get("geometry"))
            success_json["features"].append(feat)

        del feats, calendar_availability

        min_value = sys.maxsize
        max_value = -1
        for i in item_arr["polygon"]:
            if i > max_value:
                max_value = i
            if i < min_value:
                min_value = i
        interval = max_value - min_value
        if max_value >= 5:
            num = 5
        else:
            num = math.floor(max_value)
        pieces = interval / num if num > 0 else 0

        # Create marker legend
        if layer_style.get("extra_props").get("marker") and has_marker:
            success_json["items"]["marker"].append(layer_style.get("extra_props").get("marker"))

        # Create polygon legend
        for i in range(num):
            target = min_value + (pieces * i)
            next_value = min_value + (pieces * (i + 1))
            item = {
                "color": color_scale["polygon"][i],
                "name": f"{math.ceil(target)} - {math.floor(next_value)}",
            }
            success_json["items"]["polygon"].append(item)
            target += 1
        if feat_none:
            item = {
                "name": "no_data",
                "color": "hsl(240, 100%, 50%)"
            }
            success_json["items"]["polygon"].append(item)

        # Create point legend
        for k in color_scale.get("point"):
            if k in point_color_list:
                item = {
                    "color": color_scale["point"][k].get("color"),
                    "name": k
                }
                success_json["items"]["point"].append(item)

        # Coloring features
        for feat in success_json["features"]:
            style_color = self.calc_color(feat, min_value, max_value, color_scale, num, feat_point_color.get(feat.get("id")))
            feat["style"] = style_color
        return success_json

    def calc_color(self, feat, min_value, max_value, color_scale, num, field_key):
        feat_type = feat.get("type").lower()
        feat_style = feat.get("style")
        if feat_type == "polygon":
            style_color = self.calc_heatmap(min_value, max_value,
                                            feat.pop("total_value") if "total_value" in feat else 0, color_scale.get("polygon"), num)
            if "color" in feat_style.keys():
                feat_style["color"] = style_color
                feat_style["fillColor"] = style_color
        elif feat_type == "point":
            if field_key:
                feat_style = color_scale["point"][field_key]
        return feat_style

    def update_feature_by_id(self, feature_id: str, feature_data: FeaturePatch) -> Feature:
        feat = (
            db.session.query(Feature)
            .filter(Feature.id == feature_id)
            .filter(Feature.tenant_id == feature_data.tenant_id)
            .first()
        )
        # TODO validar lógica de recriação/deleção de FieldConfigOptions
        tenant_id = feature_data.tenant_id
        feat_dict = feature_data.dict(exclude_unset=True)
        feat_dict.pop("fields")
        language = feat_dict.pop("language")
        for k in feat_dict.keys():
            if feat.__getattribute__(k) != feat_dict.get(k):
                g.audit_data['data'].append({
                    'attribute': k,
                    'old_value': feat.__getattribute__(k),
                    'new_value': feat_dict.get(k)
                })
                feat.__setattr__(k, feat_dict.get(k))
        fields_data = feature_data.fields
        feature_fields = feat.fields
        new_fields = []
        fco_list = []
        for field_req in fields_data:
            found = 0
            for field_feat in feature_fields:
                if str(field_feat.field_config_id) == str(field_req.field_config_id):
                    found = 1
                    if field_feat.key != field_req.key:
                        g.audit_data['data'].append({
                            'attribute': field_feat.fieldconfig.key,
                            'old_value': field_feat.key,
                            'new_value': field_req.key
                        })
                        if self.check_amount_keys_in_field(field_feat.key, field_feat.field_config_id, tenant_id) <= 1:
                            db.session.query(FieldConfigOptions).filter(
                                FieldConfigOptions.field_config_id == field_feat.field_config_id).filter(
                                FieldConfigOptions.key == field_feat.key).filter(
                                FieldConfigOptions.tenant_id == tenant_id).delete()
                        field_feat.key = field_req.key
                        if self.check_amount_keys_in_field(field_feat.key, field_feat.field_config_id, tenant_id) == 0:
                            fco = FieldConfigOptions(tenant_id, key=field_feat.key, field_config_id=field_feat.field_config_id, label={language: field_feat.key})
                            fco_list.append(fco)
                    if str(field_feat.value) != str(field_req.value):
                        g.audit_data['data'].append({
                            'attribute': field_feat.key,
                            'old_value': field_feat.value,
                            'new_value': field_req.value
                        })
                        field_feat.key = field_req.key
                    new_fields.append(field_feat)
                    break
            if not found:
                field_conf = db.session.query(FieldConfig.key).filter(FieldConfig.id == field_req.field_config_id).first()
                if field_req.value is None:
                    field_req.value = 1
                g.audit_data['data'].append({
                    'attribute': field_conf.key,
                    'old_value': None,
                    'new_value': field_req.key
                })
                g.audit_data['data'].append({
                    'attribute': field_req.key,
                    'old_value': None,
                    'new_value': field_req.value
                })
                new_field = Field(**field_req.dict(), tenant_id=feature_data.tenant_id)
                new_fields.append(new_field)
        feat.fields.clear()
        feat.fields.extend(new_fields)
        db.session.add_all(fco_list)
        db.session.commit()
        return feat

    @staticmethod
    def calc_heatmap(min_value, max_value, value, color_scale, amount=5):
        steps = int(max_value)/amount if int(max_value) > 0 else 0
        value = int(value)
        h = 0
        for i in range(amount):
            cur_value = min_value
            if cur_value <= value < min_value + (steps * (i+1)):
                h = i
                break
        return color_scale[h]

    def get_chart_by_feature(self, feat_id: str, feat_data: FeatureClick, tenant):
        tabs = db.session.query(Tab).filter(Tab.tenant_id == tenant).all()
        tabs_json = {'tabs': []}
        resp = []
        for tab in tabs:
            charts = (
                db.session.query(Chart)
                .join(ChartType, ChartType.id == Chart.charttype_id)
                .join(ChartTypeTabLayer, ChartType.id == ChartTypeTabLayer.charttype_id)
                .filter(ChartTypeTabLayer.tab_id == tab.id)
                .filter(ChartTypeTabLayer.layer_id == feat_data.id_layer)
                .all()
            )
            chart_resp = []
            for chart in charts:
                formatted_query = chart.query_sql.format(
                    feat_id, feat_data.dt_start, feat_data.dt_end
                )  # TODO adicionar o `feat_data.fields`
                result = db.session.execute(formatted_query).fetchall()
                # TODO tratar o resultado
                chart_json = {'options': result[0][0]['options'], 'style': chart.style, 'visible': chart.visible,
                              'type': chart.charttype_id, 'name': chart.key}
                chart_resp.append(chart_json)

            temp = {"name": tab.key, "label": tab.label, "charts": chart_resp, 'visible': tab.visible, 'selected': tab.selected, 'style': tab.style}
            resp.append(temp)
        tabs_json['tabs'] = resp
        return tabs_json

    def create_feature_new(self, feature_data: FeaturePost) -> Feature:
        feature = Feature(**feature_data.dict(by_alias=True))
        options = {}

        # Field Creation
        for field in feature_data.fields:
            f = Field(**field.dict(by_alias=True), tenant_id=feature_data.tenant_id)
            if feature_data.type == "MARKER":
                f.value = 1
            if f.field_config_id not in options:
                options[f.field_config_id] = [f.key]
            else:
                options[f.field_config_id].append(f.key)
            feature.fields.append(f)

        # Creating properties and adding style defined in the layer
        if feature_data.type == "MARKER":
            style_data = {"icon": feature_data.properties.icon}
            props = Properties(feature_data.tenant_id, style=json.dumps(style_data), **feature_data.properties.dict())
            feature.properties.append(props)

        # Creating field config options, if it doesn't already exists
        fco_list = []
        for k in options.keys():
            found = (
                db.session.query(FieldConfigOptions)
                .filter(FieldConfigOptions.field_config_id == k)
                .filter(FieldConfigOptions.key.in_(options.get(k)))
                .all()
            )
            for fco in found:
                options.get(k).remove(fco.key)
            for create_fco in options.get(k):
                fco_ent = FieldConfigOptions(
                    feature_data.tenant_id,
                    key=create_fco,
                    field_config_id=k,
                    label={feature_data.language: create_fco},
                )
                fco_list.append(fco_ent)

        db.session.add(feature)
        db.session.add_all(fco_list)
        db.session.commit()
        return feature

    def delete_feature_by_id(self, feature_id, tenant_id):
        feat = self.get_feature_by_id(feature_id, tenant_id)
        db.session.query(Properties).filter(feat.id == Properties.feature_id).delete()
        for field in feat.fields:
            if self.check_amount_keys_in_field(field.key, field.field_config_id, tenant_id) <= 1:
                db.session.query(FieldConfigOptions).filter(FieldConfigOptions.field_config_id == field.field_config_id).filter(FieldConfigOptions.key == field.key).filter(FieldConfigOptions.tenant_id == tenant_id).delete()
        db.session.query(Field).filter(Field.feature_id == feature_id).filter(Field.tenant_id == tenant_id).delete()
        db.session.delete(feat)
        db.session.commit()
        return feat

    def check_amount_keys_in_field(self, key, field_config_id, tenant_id):
        return db.session.query(func.count(Field.id)).filter(Field.key == key).filter(Field.field_config_id == field_config_id).filter(Field.tenant_id == tenant_id).scalar()

    def get_feature_by_id(self, feature_id, tenant_id):
        feat = db.session.query(Feature).filter(Feature.id == feature_id).filter(Feature.tenant_id == tenant_id).first()
        if feat:
            return feat
        raise EntityNotFound
