from ext import db
from enum import IntEnum
from sqlalchemy.dialects.postgresql import SMALLINT
from datetime import datetime


class Tenant(db.Model):
    __tablename__ = 'Tenant'
    __table_args__ = ({'schema': 'web'})
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    city = db.Column(db.String(255))
    city_code = db.Column(db.String(255))
    country = db.Column(db.String(255))
    status = db.Column(SMALLINT)
    # domain = db.Column(db.String(255))
    # map_type = db.Column(db.String(255))
    # bucket_url = db.Column(db.String(255))
    # theme = db.Column(db.String(255))
    # tenant_status = db.Column(SMALLINT)
    last_update = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<{klass} {id} {attrs}>".format(
            klass=self.__class__.__name__,
            id=id(self) & 0xFFFFFF,
            attrs=" ".join("{}={!r}".format(k, v) for k, v in self.__dict__.items()),
        )

    @property
    def id_(self):
        return str(self.id)


class TenantStatus(IntEnum):
    SUSPENDED = 0
    ACTIVE = 1
    DELETED = 2
