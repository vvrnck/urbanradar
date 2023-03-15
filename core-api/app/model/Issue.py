from ext import db


class Issue(db.Model):
    __tablename__ = 'issue'
    __table_args__ = {'schema': 'web'}
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(), nullable=False)
    user = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    version = db.Column(db.String(100), nullable=False)
    image = db.Column(db.Text())
    origin = db.Column(db.String(3))
    status = db.Column(db.String(55))

    def __repr__(self):
        return f'<Issue {self.id}>'

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self, issue_id, date, user, title, description, version, image, status, origin):
        Issue.query.filter_by(id=issue_id).update(dict(id=id, date=date, user=user, title=title, description=description, version=version, image=image, status=status, origin=origin))
        db.session.commit()

    def patch(self, issue_id, **kwargs):
        issue = Issue.query.filter(Issue.id == issue_id).filter(Issue.origin == kwargs.get("origin")).first()
        for k in kwargs.keys():
            issue.__setattr__(k, kwargs.get(k))
        db.session.commit()