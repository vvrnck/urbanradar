from ext import db


class UserRoleTenant(db.Model):
    __tablename__ = 'UserRoleTenant'
    __table_args__ = ({'schema': 'web'})
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('web.User.id', ondelete="CASCADE"), primary_key=True)
    role_id = db.Column('role_id', db.Integer, db.ForeignKey('web.Role.id', ondelete="CASCADE"), primary_key=True)
    tenant_id = db.Column('tenant_id', db.Integer, db.ForeignKey('web.Tenant.id', ondelete="CASCADE"), primary_key=True)

    def __init__(self, user_id=None, role_id=None, tenant_id=None):
        self.user_id = user_id
        self.role_id = role_id
        self.tenant_id = tenant_id
