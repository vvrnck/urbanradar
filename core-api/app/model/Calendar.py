from ext import db
from app.model.Tenant import Tenant
from app.model.Layer import Layer
from app.model.Feature import Feature


class Calendar(db.Model):
    __tablename__ = 'Calendar'
    __table_args__ = {'schema': 'web'}
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey(Tenant.id), nullable=False)
    layer_id = db.Column(db.Integer, db.ForeignKey(Layer.id), nullable=False)
    feature_id = db.Column(db.Integer, db.ForeignKey(Feature.id), nullable=False)
    available_date = db.Column(db.Date)

    def __repr__(self):
        return f'<Calendar {self.id}>'
