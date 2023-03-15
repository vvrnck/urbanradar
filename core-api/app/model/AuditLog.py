from ext import db
from datetime import datetime
from uuid import uuid1
from app.model.User import User


class AuditLog(db.Model):
    __tablename__ = 'AuditLog'
    __table_args__ = {'schema': 'web'}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("web.User.id", ondelete="RESTRICT"))
    user_name = db.Column(db.String(100))
    action = db.Column(db.String(255))
    url = db.Column(db.String(255))
    ip = db.Column(db.String(55))
    browser = db.Column(db.String(255))

    object_type = db.Column(db.String(255))
    object_name = db.Column(db.String(255))
    object_id = db.Column(db.Integer)
    data = db.Column(db.JSON)

    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    tenant = db.Column(db.String(55), nullable=False)

    def __init__(self, object_type, object_name, object_id, user_id, action, url, data, browser, ip, user_name, tenant_id):
        self.id_ = uuid1().int >> 64
        self.object_type = object_type
        self.object_name = object_name
        self.object_id = object_id
        self.user_id = user_id
        self.action = action
        self.data = data
        self.url = url
        self.browser = browser
        self.ip = ip
        self.user_name = user_name
        self.tenant = tenant_id

    def __repr__(self):
        return f'<Log {self.id}>'
