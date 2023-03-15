from ext import db
from app.model.Feature import Feature
from app.model.Tenant import Tenant
from datetime import datetime
import uuid


class Properties(db.Model):
    __tablename__ = 'Properties'
    __table_args__ = {'schema': 'web'}
    id = db.Column(db.Integer, primary_key=True)
    feature_id = db.Column(db.Integer, db.ForeignKey(Feature.id), nullable=False, index=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey(Tenant.id), nullable=False)
    image = db.Column(db.String(255))
    style = db.Column(db.String(255))
    display_name = db.Column(db.String(255))
    label = db.Column(db.String(255))

    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_update = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, tenant_id: int, **kwargs):
        self.id = uuid.uuid1().int >> 100
        self.tenant_id = tenant_id
        self.style = kwargs.get("style")
        self.image = kwargs.get("image")
        self.display_name = kwargs.get("display_name")
        self.label = kwargs.get("label")
