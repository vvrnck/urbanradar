from ext import db
from datetime import datetime
from app.model.Tenant import Tenant


class FeatureCollection(db.Model):
    __tablename__ = 'FeatureCollection'
    __table_args__ = {'schema': 'web'}
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(255))
    active = db.Column(db.Boolean)
    bbox = db.Column(db.String(255))
    bucket_url = db.Column(db.String(255))
    tenant_id = db.Column(db.Integer, db.ForeignKey(Tenant.id), nullable=False)
    view = db.Column(db.String(255))

    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_update = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<FeatureCollection {self.name}>'
