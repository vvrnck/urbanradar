from ext import db


class RoleScope(db.Model):
    __tablename__ = 'RoleScope'
    __table_args__ = ({'schema': 'web'})
    role_id = db.Column(db.Integer, db.ForeignKey('web.Role.id', ondelete="CASCADE"), primary_key=True)
    scope_id = db.Column(db.Integer, db.ForeignKey('web.Scope.id', ondelete="CASCADE"), primary_key=True)

    def __init__(self, role_id, scope_id):
        self.role_id = role_id
        self.scope_id = scope_id
