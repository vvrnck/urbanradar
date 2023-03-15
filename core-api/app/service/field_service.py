from app.model.Field import FieldConfig, FieldConfigOptions, FieldConfigLayer
from app.serializer.field import FieldConfigPost
from ext import db


def create_field_config(fc_data: FieldConfigPost) -> FieldConfig:
    fc = FieldConfig(**fc_data.dict())
    for option in fc_data.field_config_options:
        fc_opt = FieldConfigOptions(**option.dict())
        fc.options.append(fc_opt)
    fcl = FieldConfigLayer()
    fcl.tenant_id = fc_data.tenant_id
    fcl.layer_id = fc_data.layer_id
    fc.field_config_layer.append(fcl)
    db.session.add(fc)
    db.session.commit()
    return fc
