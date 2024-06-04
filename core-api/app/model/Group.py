from ext import db


class Group(db.Model):
    __tablename__ = 'Group'

    __table_args__ = {'schema': 'web'}

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(55), nullable=False)
    origin = db.Column(db.String(3), nullable=False)

    def __repr__(self):
        return f'<Group>'
