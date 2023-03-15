from ext import db
from datetime import datetime


class Scope(db.Model):
    __tablename__ = 'Scope'
    __table_args__ = ({'schema': 'web'})
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(500))
    key = db.Column(db.String(500))
    name = db.Column(db.String(500))
    last_update = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    creation_date = db.Column(db.DateTime)

    @property
    def id_(self):
        return str(self.id)
