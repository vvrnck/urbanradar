from ext import db
from sqlalchemy.dialects.postgresql import JSONB


class Filter(db.Model):
    __tablename__ = 'filter'
    __table_args__ = {'schema': 'web'}
    id = db.Column(db.Integer, primary_key=True)
    id_layer = db.Column(db.Integer, nullable=False)
    id_group = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Filter>'


class GenericQueries(db.Model):
    __tablename__ = 'generic_queries'
    __table_args__ = {'schema': 'web'}
    query_key = db.Column(db.TEXT, primary_key=True)
    tenant = db.Column(db.TEXT, primary_key=True)
    type_ = db.Column("type", db.TEXT)
    query_sql = db.Column(db.TEXT)
    filters = db.Column(JSONB)
    layers = db.Column(JSONB)

    def __repr__(self):
        return f'<CCTV {self.query_key}>'


class RawCCTVHex(db.Model):
    __tablename__ = 'cctv_hex'
    __table_args__ = {'schema': 'datalake_ct'}
    ref = db.Column("Reference", db.TEXT, primary_key=True)
    index = db.Column(db.TEXT)

    def __repr__(self):
        return f'<CCTV Hex {self.ref}>'


class Profile(db.Model):
    __tablename__ = 'profile'
    __table_args__ = {'schema': 'web'}
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(55), primary_key=True)
    name = db.Column(db.String(55))
    email = db.Column(db.String(55), nullable=False)
    role = db.Column(db.String(55), nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)
    origin = db.Column(db.String(55))

    def __repr__(self):
        return f'<Profile {self.code}>'

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self, uid, name, role, active, origin):
        Profile.query.filter_by(uid=uid).update(dict(name=name, role=role, active=active, origin=origin))
        db.session.commit()


class Section(db.Model):
    __tablename__ = 'section'
    __table_args__ = {'schema': 'web'}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(55))
    icon = db.Column(db.String(55))
    position = db.Column(db.Integer)
    origin = db.Column(db.String(55))

    def __repr__(self):
        return f'<Section {self.id}>'


class SectionLayer(db.Model):
    __tablename__ = 'section_layer'
    __table_args__ = {'schema': 'web'}
    id = db.Column(db.Integer, primary_key=True)
    id_section = db.Column(db.Integer)
    id_layer = db.Column(db.Integer)

    def __repr__(self):
        return f'<Section_Layer {self.id}>'


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


class Predictions(db.Model):
    __tablename__ = 'prediction_precision'
    __table_args__ = {'schema': 'web'}
    n_sectors = db.Column(db.String(55))
    algorithm = db.Column(db.String(55))
    model_date = db.Column(db.String(55))
    run_time = db.Column(db.String(55))
    f1 = db.Column(db.String(55))
    f1_threshold = db.Column(db.String(55))
    f2 = db.Column(db.String(55))
    f2_threshold = db.Column(db.String(55))
    training_start = db.Column(db.String(55))
    training_end = db.Column(db.String(55))
    prediction_for = db.Column(db.String(55))
    model_path = db.Column(db.String(55))
    observation = db.Column(db.String(55))
    layer = db.Column(db.String(55), primary_key=True)
    prediction_date = db.Column(db.String(55), primary_key=True)

    def __repr__(self):
        return f'<Predictions>'


class Field(db.Model):
    __tablename__ = 'field'
    __table_args__ = {'schema': 'web'}
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(55))
    value = db.Column(db.String(55))
    type_ = db.Column("type", db.String(55))
    origin = db.Column(db.String(55))

    def __repr__(self):
        return f'<Fields {self.id}>'


class UnavailableDates(db.Model):
    __tablename__ = 'unavailable_dates'
    __table_args__ = {'schema': 'web'}
    origin = db.Column(db.String(55))
    id_layer = db.Column(db.BIGINT, primary_key=True)
    dt_filter = db.Column(db.String(55))

    def __repr__(self):
        return f'<Fields {self.id}>'

