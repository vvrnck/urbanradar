from ext import db
from sqlalchemy import and_
from app.model.Field import FieldConfigOptions
from app.model.Layer import Layer, Section
from app.model.Field import FieldConfigLayer, FieldConfig
from app.serializer.layer import LayerPost
from sqlalchemy import func
from app.util.exceptions import EntityNotFound


class LayerService:
    @staticmethod
    def list_layer(tenant):
        sections = (
            db.session.query(
                Section.id,
                func.json_build_object(
                    "id",
                    Section.id,
                    "icon",
                    Section.icon,
                    "order",
                    Section.order,
                    "label",
                    Section.label,
                    "layers",
                    func.json_agg(
                        func.json_build_object(
                            "id",
                            Layer.id,
                            "name",
                            Layer.name,
                            "selected",
                            Layer.selected,
                            "order",
                            Layer.order,
                            "selected",
                            Layer.selected,
                            "editable",
                            Layer.editable,
                            "style",
                            Layer.style,
                            "label",
                            Layer.label,
                            "active",
                            Layer.active,
                            "configurable",
                            Layer.configurable,
                        )
                    ),
                ),
            )
                .join(Layer, Layer.id_section == Section.id)
                .filter(Section.tenant == tenant)
                .order_by(Section.order)
                .group_by(Section.id)
                .all()
        )
        success_json = []
        for sec in sections:
            section = sec[1]
            section["layers"] = sorted(section["layers"], key=lambda x: x.get("order"))
            for layer in section.get("layers"):
                field_config_list = (
                    db.session.query(
                        func.json_build_object(
                            "id",
                            FieldConfig.id,
                            "type",
                            FieldConfig.type,
                            "name",
                            FieldConfig.key,
                            "label",
                            FieldConfig.label,
                            "visible",
                            FieldConfig.visible,
                            "tags",
                            func.json_build_array(),
                            "value",
                            "",
                            "values",
                            func.json_build_array(),
                            "order",
                            FieldConfig.order,
                            "items",
                            func.json_agg(
                                func.json_build_object(
                                    "id",
                                    FieldConfigOptions.id,
                                    "text",
                                    FieldConfigOptions.key,
                                    "label",
                                    FieldConfigOptions.label,
                                    "selected",
                                    False,
                                )
                            ),
                            "mobileItems",
                            func.json_agg(
                                func.json_build_object(
                                    "id",
                                    FieldConfigOptions.id,
                                    "text",
                                    FieldConfigOptions.key,
                                    "label",
                                    FieldConfigOptions.label,
                                    "selected",
                                    False,
                                )
                            ),
                        )
                    )
                        .join(
                        FieldConfigLayer,
                        and_(
                            FieldConfigLayer.fieldconfig_id == FieldConfig.id,
                            FieldConfigLayer.layer_id == layer.get("id"),
                        ),
                    )
                        .join(
                        FieldConfigOptions,
                        FieldConfigOptions.field_config_id == FieldConfig.id,
                    )
                        .order_by(FieldConfig.order)
                        .group_by(FieldConfig.id)
                        .all()
                )
                layer["filters"] = []
                for field_config in field_config_list:
                    layer["filters"].append(field_config[0])
                # Append filters
            success_json.append(section)
        return success_json

    @staticmethod
    def delete_feature_delete_properties(id_feature, id_layer, origin):
        feat_to_delete = (
            Feature.query.filter(Feature.id == id_feature)
                .filter(Feature.id_layer == id_layer)
                .filter(Feature.origin == origin)
                .first()
        )

        props_to_delete = Properties.query.filter(
            Properties.id_feature == id_feature
        ).all()

        for prop in props_to_delete:
            db.session.delete(prop)
        db.session.commit()

        db.session.delete(feat_to_delete)
        db.session.commit()

        success_json = {"id": feat_to_delete.id}
        return success_json

    def create_layer(self, layer_data: LayerPost) -> Layer:
        layer = Layer(**layer_data.dict(by_alias=True))
        db.session.add(layer)
        db.session.commit()
        return layer

    def delete_layer_by_id(self, layer_id: str, tenant_id: int) -> bool:
        db.session.query(Layer).filter(Layer.id == layer_id).filter(
            Layer.tenant == tenant_id
        ).delete()
        db.session.commit()
        return True

    def get_layer_by_id(self, layer_id: str, tenant_id: int) -> Layer:
        layer = (
            db.session.query(Layer)
                .filter(Layer.id == layer_id)
                .filter(Layer.tenant == tenant_id)
                .first()
        )
        if not layer:
            raise EntityNotFound
        return layer

    def update_layer_by_id(self, layer_id: str, tenant_id: int, layer_data: LayerPost) -> Layer:
        layer = self.get_layer_by_id(layer_id, tenant_id)
        layer_dict = layer_data.dict(by_alias=True, exclude_unset=True)
        for data in layer_dict:
            layer.__setattr__(data, layer_dict.get(data))
        db.session.commit()
        return layer
