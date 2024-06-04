from ext import db
from datetime import datetime
import uuid


class User(db.Model):
    __tablename__ = 'User'
    __table_args__ = ({'schema': 'web'})
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=False)
    uid = db.Column(db.String(200))
    name = db.Column(db.String(500))
    email = db.Column(db.String(200), unique=True)
    active = db.Column(db.Boolean)
    last_update = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)

    user_role_tenant = db.relationship("UserRoleTenant", lazy='select', cascade="all, save-update, delete, delete-orphan")

    def __init__(self, id, uid, name, email, active, **kwargs):
        self.id = id
        self.uid = uid
        self.name = name
        self.email = email
        self.active = active
