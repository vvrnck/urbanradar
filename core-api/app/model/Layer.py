import uuid
from ext import db
from app.model.Tenant import Tenant
from datetime import datetime


class Section(db.Model):
    __tablename__ = 'Section'
    __table_args__ = {'schema': 'web'}
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    tenant = db.Column(db.Integer, db.ForeignKey(Tenant.id), nullable=False)
    name = db.Column(db.String(255))
    icon = db.Column(db.String(255))
    order = db.Column(db.Integer)
    label = db.Column(db.JSON())

    layers = db.relationship('Layer', cascade='all, save-update, delete, delete-orphan', lazy="joined")

    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_update = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, **kwargs):
        self.id = uuid.uuid1().int >> 100
        self.name = kwargs.get("name")
        self.tenant = kwargs.get("tenant")
        self.icon = kwargs.get("icon")
        self.order = kwargs.get("order")
        self.label = kwargs.get("label")

    def __repr__(self):
        return f'<Section {self.name}>'


class Layer(db.Model):
    __tablename__ = 'Layer'
    __table_args__ = {'schema': 'web'}
    id = db.Column(db.Integer, autoincrement=False, primary_key=True)
    tenant = db.Column(db.Integer, db.ForeignKey(Tenant.id), nullable=False)
    id_section = db.Column(db.Integer, db.ForeignKey(Section.id), nullable=False)
    name = db.Column(db.String(255))
    selected = db.Column(db.Boolean())
    order = db.Column(db.Integer)
    active = db.Column(db.Boolean())
    style = db.Column(db.JSON())
    editable = db.Column(db.Boolean())
    label = db.Column(db.JSON())

    configurable = db.Column(db.Boolean())

    section = db.relationship(Section, lazy="joined")
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_update = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, **kwargs):
        self.id = uuid.uuid1().int >> 100
        self.name = kwargs.get("name")
        self.tenant = kwargs.get("tenant")
        self.id_section = kwargs.get("id_section")
        self.selected = kwargs.get("selected")
        self.order = kwargs.get("order")
        self.active = kwargs.get("active")
        self.style = kwargs.get("style")
        self.editable = kwargs.get("editable")
        self.label = kwargs.get("label")
        self.configurable = kwargs.get("configurable")

    def __repr__(self):
        return f'<Layer {self.name}>'
