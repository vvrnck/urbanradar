from app import db


class Feedback(db.Model):
    __tablename__ = 'Feedback'
    __table_args__ = {'schema': 'web'}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    filename = db.Column(db.Text())
    b64file = db.Column(db.Text())
    user_uid = db.Column(db.String(100))
    user_name = db.Column(db.String(100))
    tenant = db.Column(db.String(55))
    browser = db.Column(db.String(255))

    def __repr__(self):
        return f'<Feedback {self.title}>'
