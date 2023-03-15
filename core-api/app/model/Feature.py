from ext import db
from datetime import datetime
from app.model.Tenant import Tenant
from app.model.Layer import Layer
import uuid
from app.model.FeatureCollection import FeatureCollection


class Feature(db.Model):
    __tablename__ = 'Feature'
    __table_args__ = {'schema': 'web'}
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    code = db.Column(db.String(255))
    tenant_id = db.Column(db.Integer, db.ForeignKey(Tenant.id), nullable=False)
    layer_id = db.Column(db.Integer, db.ForeignKey(Layer.id), nullable=False, index=True)
    feature_collection_id = db.Column(db.Integer, db.ForeignKey(FeatureCollection.id), nullable=False)
    geometry = db.Column(db.String(1000), nullable=False)
    type = db.Column(db.String(255))
    view = db.Column(db.String(255))

    fields = db.relationship('app.model.Field.Field', cascade='all, save-update, delete, delete-orphan', lazy="joined")
    properties = db.relationship('Properties', cascade='all, save-update, delete, delete-orphan', lazy="joined")

    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_update = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, tenant_id: int, **kwargs):
        self.id = uuid.uuid1().int >> 100
        self.layer_id = kwargs.get("layer_id")
        self.code = kwargs.get("code")
        self.geometry = kwargs.get("geometry")
        self.feature_collection_id = kwargs.get("feature_collection_id")
        self.tenant_id = tenant_id
        self.type = kwargs.get("type")

    def __repr__(self):
        return f'<Feature {self.code}>'
