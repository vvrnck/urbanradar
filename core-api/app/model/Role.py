from ext import db
from datetime import datetime
import uuid


class Role(db.Model):
    __tablename__ = 'Role'
    __table_args__ = ({'schema': 'web'})
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=False)
    name = db.Column(db.String, unique=True)
    default = db.Column(db.Boolean)
    last_update = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)

    tenant_id = db.Column(db.Integer, db.ForeignKey("web.Tenant.id"), nullable=False)

    users = db.relationship("User", secondary="web.UserRoleTenant", lazy="joined")
    scopes = db.relationship("RoleScope", lazy='joined', cascade="all, save-update, delete, delete-orphan")
    scopes_entity = db.relationship("Scope", secondary="web.RoleScope", lazy='joined')

    @property
    def id_(self):
        return str(self.id)

    def __init__(self, name, tenant_id, **kwargs):
        self.id = uuid.uuid1().int >> 100
        self.name = name
        self.default = False
        self.tenant_id = tenant_id
