from ext import db
from app.model.Feature import Feature
from app.model.Tenant import Tenant
from app.model.Layer import Layer
import uuid


class FieldConfig(db.Model):
    __tablename__ = 'FieldConfig'
    __table_args__ = ({'schema': 'web'})
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey(Tenant.id))

    key = db.Column(db.String(255))
    label = db.Column(db.JSON)
    visible = db.Column(db.Boolean)
    order = db.Column(db.Integer)
    type = db.Column(db.String(255))

    options = db.relationship('FieldConfigOptions', cascade='all, save-update, delete, delete-orphan', lazy="joined")
    field_config_layer = db.relationship('FieldConfigLayer', cascade='all, save-update, delete, delete-orphan', lazy="joined")

    def __init__(self, **kwargs):
        self.id = uuid.uuid1().int >> 100
        self.key = kwargs.get("key")
        self.label = kwargs.get("label")
        self.visible = kwargs.get("visible")
        self.order = kwargs.get("order")
        self.tenant_id = kwargs.get("tenant_id")
        self.type = kwargs.get("type")


class Field(db.Model):
    __tablename__ = 'Field'
    __table_args__ = ({'schema': 'web'})
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    field_config_id = db.Column(db.Integer, db.ForeignKey(FieldConfig.id), index=True)
    feature_id = db.Column(db.Integer, db.ForeignKey(Feature.id), index=True)
    date = db.Column(db.Date, index=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey(Tenant.id), index=True)

    key = db.Column(db.String(255))
    value = db.Column(db.String(255))
    extra_props = db.Column(db.JSON)

    fieldconfig = db.relationship(FieldConfig, backref=db.backref('fieldconfig', lazy='select'))

    def __init__(self, key, value, field_config_id, tenant_id, **kwargs):
        self.id = uuid.uuid1().int >> 100
        self.key = key
        self.value = value
        self.field_config_id = field_config_id
        self.tenant_id = tenant_id
        self.extra_props = kwargs.get("extra_props")

    def __repr__(self):
        return f'<Field {self.id}>'


class FieldConfigOptions(db.Model):
    __tablename__ = 'FieldConfigOptions'
    __table_args__ = ({'schema': 'web'})
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    field_config_id = db.Column(db.Integer, db.ForeignKey(FieldConfig.id))
    tenant_id = db.Column(db.Integer, db.ForeignKey(Tenant.id))
    key = db.Column(db.String(255))
    label = db.Column(db.JSON)

    def __init__(self, tenant_id: int, **kwargs):
        self.id = uuid.uuid1().int >> 100
        self.key = kwargs.get("key")
        self.label = kwargs.get("label")
        self.field_config_id = kwargs.get("field_config_id")
        self.tenant_id = tenant_id


class FieldConfigLayer(db.Model):
    __tablename__ = 'FieldConfigLayer'
    __table_args__ = {'schema': 'web'}

    layer_id = db.Column(db.Integer, db.ForeignKey(Layer.id), primary_key=True)
    fieldconfig_id = db.Column(db.Integer, db.ForeignKey(FieldConfig.id), primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey(Tenant.id), primary_key=True)

    fieldconfig = db.relationship(FieldConfig, backref=db.backref('fieldconfigs', lazy='select'))
    layer = db.relationship(Layer, backref=db.backref('fieldconfiglayers', lazy='select'))

    def __repr__(self):
        return f'<FieldConfigLayer {self.fieldconfig_id}>'
