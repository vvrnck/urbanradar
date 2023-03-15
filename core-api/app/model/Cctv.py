from ext import db


class OptimizationCCTV(db.Model):
    __tablename__ = 'otimization_cctv'
    __table_args__ = {'schema': 'datalake_ct'}
    cctv_unit = db.Column(db.String())
    category_2 = db.Column(db.String())
    shift = db.Column(db.String())
    cameras_persona = db.Column(db.Integer())
    operators_persona = db.Column(db.Integer())
    incident_weekday = db.Column(db.String())
    incident_week = db.Column(db.Integer())
    supervisor_name = db.Column(db.String())
    cameras_id = db.Column(db.String())
    operators_id = db.Column(db.Integer())
    cameras_persona_category_2 = db.Column(db.Integer())
    operators_persona_category_2 = db.Column(db.Integer())
    category_2_incidents = db.Column(db.Integer())
    efficiency = db.Column(db.Integer())
    benchmark = db.Column(db.Integer())
    decision_making_unit = db.Column(db.String())
    dmu_coeff = db.Column(db.Integer())
    potential_output_improvement_percentual = db.Column(db.Integer())
    category_2_incidents_target = db.Column(db.Integer())
    optm_date = db.Column(db.String())
    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return f'<Optimization {self.id}>'


class CCTVConsoles(db.Model):
    __tablename__ = 'cctv_consoles'
    __table_args__ = {'schema': 'datalake_ct'}
    id_camera = db.Column("id_camera", db.TEXT, primary_key=True)
    console_number = db.Column("console_number", db.BIGINT)
    name = db.Column("name", db.TEXT)

    def __repr__(self):
        return f'<CCTV {self.id_camera}>'


class CCTVCameras(db.Model):
    __tablename__ = 'cctv_cameras'
    __table_args__ = {'schema': 'datalake_ct'}
    camera_number = db.Column("Camera NR", db.TEXT, primary_key=True)
    ref = db.Column("Reference", db.TEXT)

    def __repr__(self):
        return f'<CCTV Cameras {self.camera_number}>'


class RawCCTV(db.Model):
    __tablename__ = 'cctv'
    __table_args__ = {'schema': 'datalake_ct'}
    id = db.Column(db.BIGINT, primary_key=True)
    reference = db.Column("Reference", db.TEXT)
    camera_suburb = db.Column("Camera Suburb", db.TEXT)
    camera_id = db.Column("Camera ID", db.TEXT)
    responded_to_by = db.Column("Responded To By", db.TEXT)
    arrests_made = db.Column("Arrests Made", db.TEXT)
    n_arrests = db.Column("No. of Arrests", db.TEXT)
    cat_one = db.Column("Category 1", db.TEXT)
    cat_two = db.Column("Category 2", db.TEXT)
    cat_three = db.Column("Category 3", db.TEXT)
    cat_four = db.Column("Category 4", db.TEXT)
    incident_date = db.Column("Incident Date", db.TEXT)
    incident_time = db.Column("Incident Time", db.TEXT)
    supervisor_bp = db.Column("Supervisor BP No.", db.TEXT)
    supervisor_name = db.Column("Supervisor Name", db.TEXT)
    user_status = db.Column("User Status", db.TEXT)
    operator = db.Column("Operator", db.TEXT)
    posting_date = db.Column("Posting Date", db.TEXT)
    responded_to_by_two = db.Column("Responded To By (2)", db.TEXT)
    incident_clear_at = db.Column("Incident Clear At", db.TEXT)
    police_station = db.Column("Police Station", db.TEXT)
    comments = db.Column("Comments", db.TEXT)
    camera_nr = db.Column("Camera NR", db.TEXT)
    camera_suburb_two = db.Column("Camera Suburb2", db.TEXT)
    camera_location = db.Column("Camera Location", db.TEXT)
    cctv_unit = db.Column("CCTV Unit", db.TEXT)
    consoles = db.Column("Consoles", db.TEXT)
    time = db.Column("Time", db.TEXT)
    day_of_week = db.Column("Day of week", db.TEXT)
    month = db.Column("Month", db.TEXT)
    mnths = db.Column("MNTHS", db.TEXT)
    year = db.Column("Year", db.TEXT)
    area = db.Column("Area", db.TEXT)
    sub_council = db.Column("SUB-COUNCIL", db.TEXT)
    ward = db.Column("WARD", db.TEXT)
    absda = db.Column("ABSDA", db.TEXT)
    x_cordinates = db.Column("X-Cordinates", db.TEXT)
    y_cordinates = db.Column("Y-Cordinates", db.TEXT)
    type = db.Column("TYPE", db.TEXT)

    def __repr__(self):
        return f'<CCTV {self.id}>'
