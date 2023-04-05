from ext import db
from sqlalchemy.dialects.postgresql import JSONB


class Dashboard(db.Model):
    __tablename__ = 'Dashboard'
    __table_args__ = ({'schema': 'web'})
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(55))
    dt_created = db.Column(db.DATE)
    origin = db.Column(db.String(55))
    layout_grid = db.Column(db.JSON)

    def __repr__(self):
        return f'<Dashboard {self.id}>'


class DashboardItem(db.Model):
    __tablename__ = 'DashboardItem'
    __table_args__ = ({'schema': 'web'})
    id = db.Column(db.Integer, primary_key=True)
    id_dashboard = db.Column(db.Integer, db.ForeignKey('web.Dashboard.id'))
    tipo = db.Column(db.String(55))
    titulo = db.Column(db.String(55))
    sql = db.Column(db.String(255))
    filters = db.Column(db.JSON)
    grid_line = db.Column(db.String(255))
    grid_col = db.Column(db.String(255))

    def __repr__(self):
        return f'<DashboardItem {self.id}>'
