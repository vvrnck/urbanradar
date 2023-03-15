from ext import db
from datetime import datetime
from app.model.Tenant import Tenant
from app.model.Layer import Layer
from app.model.FeatureCollection import FeatureCollection


class Tab(db.Model):
    __tablename__ = 'Tab'
    __table_args__ = {'schema': 'web'}
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey(Tenant.id), nullable=False)
    key = db.Column(db.String(255))
    label = db.Column(db.JSON)
    priority = db.Column(db.Integer)
    visible = db.Column(db.Boolean)
    selected = db.Column(db.Boolean)
    style = db.Column(db.TEXT)

    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_update = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Tab {self.id}>'


class ChartType(db.Model):
    __tablename__ = 'ChartType'
    __table_args__ = {'schema': 'web'}
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey(Tenant.id), nullable=False)
    key = db.Column(db.String(255))
    extra_props = db.Column(db.TEXT)

    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_update = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<ChartType {self.id}>'


class Chart(db.Model):
    __tablename__ = 'Chart'
    __table_args__ = {'schema': 'web'}
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey(Tenant.id), nullable=False)
    charttype_id = db.Column(db.Integer, db.ForeignKey(ChartType.id), nullable=False)
    label = db.Column(db.JSON)
    key = db.Column(db.String(255))
    query_sql = db.Column(db.TEXT)
    visible = db.Column(db.Boolean)
    style = db.Column(db.TEXT)

    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_update = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Chart {self.id}>'


class ChartTypeTabLayer(db.Model):
    __tablename__ = 'ChartTypeTabLayer'
    __table_args__ = {'schema': 'web'}
    charttype_id = db.Column(db.Integer, db.ForeignKey(ChartType.id), primary_key=True)
    tab_id = db.Column(db.Integer, db.ForeignKey(Tab.id), primary_key=True)
    layer_id = db.Column(db.Integer, db.ForeignKey(Layer.id), primary_key=True)

    def __repr__(self):
        return f'<ChartTypeTabLayer {self.tab_id}>'
