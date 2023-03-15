import json
import os
from flask import request, jsonify
from webargs.flaskparser import use_args
from ext import db
from app.models import Profile, Dashboard, DashboardItem, Predictions, Field
from app.model.Field import Field
from app.serializers import *
from app.util.decorators import authentication
from app.util_services import generate_chart_options
from app.service.optimization_service import OptimizationService
from flask import Blueprint

api_bp = Blueprint('api', __name__, url_prefix='/api/v1/')


@api_bp.route('/groups')
@authentication
def list_groups(**kwargs):
    json_return = {"data": [
        {"id": 'abc', "name": "Operacional Setor 1"},
        {"id": "def", "name": "Operacional Setor 2"}
    ]}
    # try:
    #   management_service = ManagementService()
    # except Exception as err:
    #   logging_client.log_struct(log_struct.message.a)

    return json_return


@api_bp.route('/status')
def status():
    return jsonify({
        'status': 'ok',
        'version': '47786e19575e4d8d8e36d4c1cd2ed1a1'
    })


@api_bp.route('/avaiabledates')
@use_args(LayerSerializer)
@authentication
def dates(args, **kwargs):
    origin = args['origin']

    sql_a = """
        SELECT 
            id_layer,
            dt_filter
        FROM web.available_dates
        WHERE
            origin = '{}'
        GROUP BY 1,2
        ORDER BY 1
    """.format(origin)

    sql_u = """
        SELECT 
            id_layer,
            dt_filter
        FROM web.unavailable_dates
        WHERE
            origin = '{}'
        GROUP BY 1,2
        ORDER BY 1
    """.format(origin)

    cursor = db.session.execute(sql_a)
    r = cursor.fetchone()

    dates = {}
    while r:
        if not dates.get(r['id_layer']):
            dates[r['id_layer']] = {'available': [], 'unavailable': []}

        dates[r['id_layer']]['available'].append(r['dt_filter'])

        r = cursor.fetchone()

    cursor = db.session.execute(sql_u)
    r = cursor.fetchone()

    while r:
        if not dates.get(r['id_layer']):
            dates[r['id_layer']] = {'available': [], 'unavailable': []}

        dates[r['id_layer']]['unavailable'].append(r['dt_filter'])
        r = cursor.fetchone()

    return dates


@api_bp.route('/profile', methods=['POST'])
@use_args(ProfileSerializer)
@authentication
def profile(args, **kwargs):
    prof = Profile(**args)
    prof.insert()
    return jsonify()


@api_bp.route('/profile', methods=['GET'])
@use_args(ProfileSerializerList)
@authentication
def profile_ret(args, **kwargs):
    origin = args.get("origin")
    profiles = Profile.query.filter(Profile.origin == origin).all()
    data = []
    for pf in profiles:
        data.append({
            'uid': pf.uid,
            'name': pf.name,
            'email': pf.email,
            'role': pf.role,
            'active': pf.active,
            'origin': pf.origin
        })
    return jsonify(data)


# Deprecated
@api_bp.route('/profilerole', methods=['GET'])
@use_args(ProfileRoleSerializer)
@authentication
def profile_get_role(args, **kwargs):
    uid = args['uid']
    pf = Profile.query.filter(Profile.uid == uid).first()
    data = [{'uid': pf.uid, 'role': pf.role}] if pf else []

    return jsonify(data)


@api_bp.route('/profilestatus', methods=['GET'])
@use_args(ProfileStatusSerializer)
@authentication
def profile_get_status(args, **kwargs):
    email = args.get("email")
    pf = Profile.query.filter(Profile.email == email).first()
    data = [{'uid': pf.uid, 'active': pf.active, 'origin': pf.origin, 'role': pf.role}] if pf else []
    return jsonify(data)


@api_bp.route('/profile', methods=['PUT'])
@use_args(ProfileSerializerUpdate)
@authentication
def profile_update(args, **kwargs):
    profile = Profile(**args)
    profile.update(**args)
    return jsonify()


@api_bp.route('/field', methods=['GET'])
@use_args(FieldSerializerList)
@authentication
def list_fields(args, **kwargs):
    origin = args.get("origin")
    type_ = args.get("type")
    answer = {"data": []}
    field_list = db.session.query(Field).filter(Field.origin == origin).filter(Field.type_ == type_).all()
    for field in field_list:
        r = {"id": field.id, "key": field.key, "value": field.value}
        answer["data"].append(r)
    return jsonify(answer)


@api_bp.route('/dashboard', methods=['GET'])
@use_args(DashboardSerializer)
@authentication
def dashboard_get(args, **kwargs):
    # select no dashboard_page, select no layout grid para pegar os charts, select nos charts (sql column) para montar eles
    page_id = args.get("page")
    origin = args.get("origin")
    item_list = args.get("item_list").split(",") if args.get("item_list") else None

    dashboard = Dashboard.query.filter(Dashboard.id == page_id).filter(Dashboard.origin == origin).first()
    layout_grid = dashboard.layout_grid

    items = DashboardItem.query.filter(DashboardItem.id_dashboard == page_id)
    if item_list:
        items = items.filter(DashboardItem.id.in_(item_list))
    items = items.all()

    charts_array = []
    count_array = []
    tables_array = []

    intervalos = [
        ("00:00:00", "05:59:59"),
        ("06:00:00", "11:59:59"),
        ("12:00:00", "17:59:59"),
        ("18:00:00", "23:59:59"),
    ]
    data_json = {}
    for item in items:
        serie = None
        headers = []
        query = item.sql
        filters_array = []
        for f in item.filters:
            if f in args.keys() and args.get(f):
                filters_array.append("\"{}\" = '{}'".format(f.upper(), args.get(f)))
        series = []
        if item.tipo.strip() == "heatmap":
            for intervalo in intervalos:
                count_array = []
                query_formatted = query.format(intervalo[0], intervalo[1],
                                               " and {}".format(" and ".join(filters_array)) if filters_array else "")
                serie = db.session.execute(query_formatted).fetchall()
                if not serie:
                    continue
                for s in serie:
                    count_value = s[1]
                    while len(count_array) != s[0]:
                        count_array.append(0)
                    count_array.append(count_value)

                serie_obj = {
                    "name": intervalo[0] + ' - ' + intervalo[1],
                    "data": count_array
                }

                series.append(serie_obj)
        elif item.tipo.strip() == "table":
            headers = [{"text": "Category 1", "value": "Category 1", "align": "start"},
                       {"text": "Category 2", "value": "Category 2", "align": "start", "groupable": False}]
            count_array = []
            query_formatted = query if not filters_array else "{} and {}".format(query, " and ".join(filters_array))
            serie = db.session.execute(query_formatted).fetchall()
            if not serie:
                break
            mes_anos = []
            categories_tuple = []
            headers_month = []
            for s in serie:
                if s.mes_ano not in mes_anos:
                    headers_month.append({"text": s.mes_ano, "value": s.mes_ano, "align": "start", "groupable": False})
                    mes_anos.append(s.mes_ano)
                cat_tuple = (s.__getattr__("Category 1"), s.__getattr__("Category 2"))
                if cat_tuple not in categories_tuple:
                    categories_tuple.append(cat_tuple)
            headers.extend(sorted(headers_month, key=lambda y: y["text"]))
            for comb in categories_tuple:
                serie_copy = serie.copy()
                count_value = {"Category 1": comb[0], "Category 2": comb[1]}
                for s in serie_copy:
                    if s.__getattr__("Category 1") == comb[0] and s.__getattr__("Category 2") == comb[1]:
                        count_value[s.mes_ano] = s.contagem
                        serie.remove(s)
                count_array.append(count_value)
        else:
            query_formatted = query if not filters_array else "{} and {}".format(query, " and ".join(filters_array))
            serie = db.session.execute(query_formatted).fetchall()
        resp_tuple = generate_chart_options(item.tipo, item.titulo, serie, intervalos, name_position=0,
                                            value_position=1)
        chart_options = resp_tuple[0]
        series = series if series else resp_tuple[1]
        if item.tipo == "table":
            output = {
                "type": item.tipo,
                "title": item.titulo,
                "position": {
                    "row": item.grid_line,
                    "col": item.grid_col
                },
                "headers": headers,
                "desserts": count_array,
                "item_id": item.id
            }
            tables_array.append(output)
        elif item.tipo == "data":
            data_json[item.titulo] = [d.__getattr__(k) for d in serie for k in d.keys()]
        else:
            output = {
                'type': item.tipo,
                'title': item.titulo,
                'position': {
                    'row': item.grid_line,
                    'col': item.grid_col
                },
                'series': series,
                'options': chart_options,
                "item_id": item.id
            }
            charts_array.append(output)

    response = {
        "data": {
            "charts": charts_array,
            "tables": tables_array
        },
        "layout": layout_grid,
        "infos": data_json
    }

    return jsonify(response)


@api_bp.route('/predictions', methods=['GET'])
@authentication
def list_predictions(**kwargs):
    predictions = Predictions.query.all()
    result = []
    for p in predictions:
        prediction = {
            "n_sectors": p.n_sectors,
            "algorithm": p.algorithm,
            "model_date": p.model_date,
            "run_time": p.run_time,
            "f1": p.f1,
            "f1_threshold": p.f1_threshold,
            "f2": p.f2,
            "f2_threshold": p.f2_threshold,
            "training_start": p.training_start,
            "training_end": p.training_end,
            "prediction_for": p.prediction_for,
            "model_path": p.model_path,
            "observation": p.observation,
            "layer": p.layer,
            "prediction_date": p.prediction_date
        }
        result.append(prediction)
    resp = {"data": result}
    return jsonify(resp)


@api_bp.route('/optimization_filters', methods=['GET'])
@use_args(OptimizationSerializer)
@authentication
def get_optimization_filters(args, **kwargs):
    ssu_unit = ['Cape Town', 'Goodwood']
    sql_supervisor = "SELECT DISTINCT split_part(supervisor_name, '/', 1) FROM datalake_ct.otimization_cctv WHERE supervisor_name NOT LIKE '%Exist%'"
    sql_operator = "SELECT DISTINCT id, name FROM datalake_ct.operator"
    sql_category = "SELECT DISTINCT category_2 FROM datalake_ct.otimization_cctv ORDER BY category_2 ASC"
    sql_camera = "SELECT DISTINCT concat(cameras_id, ': ', location) as cameras_id FROM datalake_ct.otimization_cctv o INNER JOIN datalake_ct.cctv_cameras cam on (cam.cam_id = o.cameras_id) ORDER BY cameras_id ASC"

    supervisors = []
    result_supervisor = db.session.execute(sql_supervisor).fetchall()
    for s in result_supervisor:
        supervisors.append(s[0])

    operators = []
    result_operator = db.session.execute(sql_operator).fetchall()
    for o in result_operator:
        operators.append({"id": o.id, "name": o.name})

    categorys = []
    result_category = db.session.execute(sql_category).fetchall()
    for c in result_category:
        categorys.append(c[0])

    cameras = []
    result_camera = db.session.execute(sql_camera).fetchall()
    for ca in result_camera:
        cameras.append(ca[0])

    data = {
        'ssu_unit': ssu_unit,
        'supervisors': supervisors,
        'operators': operators,
        'categorys': categorys,
        'cameras': cameras,
    }
    return jsonify(data)


@api_bp.route('/optimization1', methods=['GET'])
@authentication
def get_optimization(**kwargs):
    json_return = json.loads(os.environ.get("JSON_RESPONSE"))
    args = request.args
    org = args["origin"]
    unit = args.get("unit")
    # manager = args.get("manager")
    supervisor = args.get("supervisor_name")
    operator = args.get("operator")
    cat2 = args.get("category_2")
    camera_location = args.get("camera_location")
    camera_id = args.get("camera_id")
    shift = args.get("shift")
    # weekday = args.get("weekday")
    optimization_service = OptimizationService()
    confirmation = optimization_service.list_optimization_calendar(org, unit, supervisor, operator,
                                                                   cat2, camera_location, camera_id, shift)
    json_return["data"] = confirmation

    return json_return


@api_bp.route('/optimization', methods=['GET'])
@use_args(OptimizationSerializer)
@authentication
def get_optimization_info(args, **kwargs):
    origin = args.get("origin")
    unit = args.get("unit")
    manager = args.get("manager")
    supervisor = args.get("supervisor_name")
    operator = args.get("operator")
    category = args.get("category_2")
    camera_location = args.get("camera_location")
    camera_id = args.get("camera_id")
    shift = args.get("shift")
    weekday = args.get("weekday")

    # data = optimization_service.list_otimizations(origin)

    consoles_result = db.session.execute("SELECT DISTINCT name FROM datalake_ct.cctv_consoles ORDER BY name").fetchall()
    cameras_result = db.session.execute(
        "SELECT DISTINCT name, id_camera FROM datalake_ct.cctv_consoles GROUP BY 1,2 ORDER BY name").fetchall()

    consoles = []
    for c in consoles_result:
        cameras = []
        for cam in cameras_result:
            if (c[0] == cam[0]):
                cameras.append(cam[1])

        consoles.append({
            'name': c[0],
            'cameras': cameras
        })

    sql = """
            SELECT category_2 as category, concat(o.operators_id, ': ', op.name) as operator, supervisor_name, shift, category_2_incidents_target, cameras_id as camera_name, c.id_camera, incident_weekday, c.name as console, o.id, o.cctv_unit
            FROM datalake_ct.otimization_cctv o
            INNER JOIN datalake_ct.cctv_consoles c on (c.id_camera = o.cameras_id)
            INNER JOIN datalake_ct.operator op on (op.id = o.operators_id::text)
            --WHERE c.id_camera=split_part(o.cameras_id,':',1)
          """
    # sql = sql + " AND UPPER(name) LIKE UPPER('%{}%') ".format(unit) if unit else sql

    if (unit):
        units_sql = ''
        units = unit.split('-')
        for u in units:
            item = "'{}',".format(u)
            units_sql += item
        units_sql = units_sql[:-1]
        units_sql = " AND upper(cctv_unit) in ({})".format(units_sql)
        sql = sql + units_sql

    if (weekday):
        weekday_sql = " AND incident_weekday LIKE '%{}%' ".format(weekday)
        sql = sql + weekday_sql

    if (supervisor):
        supervisors = supervisor.split('-')
        supervisor_sql = ' AND ('
        for s in range(len(supervisors)):
            supervisor_sql = supervisor_sql + "supervisor_name LIKE '%{}%' ".format(
                supervisors[s]) if s == 0 else supervisor_sql + "OR supervisor_name LIKE '%{}%' ".format(supervisors[s])
        supervisor_sql = supervisor_sql + ")"
        sql = sql + supervisor_sql

    if (operator):
        operators = operator.split('-')
        operator_sql = ' AND ('
        for o in range(len(operators)):
            operator_sql = operator_sql + "operators_id = '{}' ".format(
                operators[o]) if o == 0 else operator_sql + "OR operators_id = '{}' ".format(operators[o])
        operator_sql = operator_sql + ')'
        sql = sql + operator_sql

    if (category):
        categorys = category.split('-')
        category_sql = ' AND ('
        for c in range(len(categorys)):
            category_sql = category_sql + "category_2 LIKE '%{}%' ".format(
                categorys[c]) if c == 0 else category_sql + "OR category_2 LIKE '%{}%' ".format(categorys[c])
        category_sql = category_sql + ')'
        sql = sql + category_sql

    if (camera_location):
        cameras = camera_location.split('-')
        camera_sql = ' AND ('
        for c in range(len(cameras)):
            camera_sql = camera_sql + "camera_id = '{}' ".format(
                cameras[c]) if c == 0 else camera_sql + "OR camera_id = '{}' ".format(cameras[c])
        camera_sql = camera_sql + ')'
        sql = sql + camera_sql

    turnos_sql = ''
    if (shift):
        turnos = shift.split('-')
        for t in turnos:
            item = "'{}',".format(t)
            turnos_sql += item
        turnos_sql = turnos_sql[:-1]
        turnos_sql = " AND shift in ({})".format(turnos_sql)
    sql = sql + turnos_sql if shift else sql

    sql = sql + " GROUP BY 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11 ORDER BY incident_weekday, shift, console, supervisor_name ASC"

    print(sql)
    result = db.session.execute(sql).fetchall()

    weekdays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    shifts = ['00:00 to 02:59', '03:00 to 05:59', '06:00 to 08:59', '09:00 to 11:59', '12:00 to 14:59',
              '15:00 to 17:59', '18:00 to 20:59', '21:00 to 23:59', ]
    data = {'Sunday': {}, 'Monday': {}, 'Tuesday': {}, 'Wednesday': {}, 'Thursday': {}, 'Friday': {}, 'Saturday': {}}

    for w in weekdays:
        for s in shifts:
            data[w][s] = {}
            for c in consoles:
                consoles_array = []
                for item in result:
                    if (item.incident_weekday == w and item.shift == s and item.console == c['name']):
                        consoles_array.append({
                            'console': c['name'],
                            'cameras': c['cameras'],
                            'operator': item.operator,
                            'category': item.category,
                            'supervisor': item.supervisor_name,
                            'camera_id': item.camera_name,
                            'goal': item.category_2_incidents_target,
                            'id': item.id
                        })
                if (len(consoles_array) > 0):
                    data[w][s][c['name']] = consoles_array

    result_response = [
        ['weekday', 'shift', 'console', 'supervisor', 'operator', 'category_2_incidents_target', 'category',
         'camera_id', 'id']]
    for r in result:
        goal = r.category_2_incidents_target
        internal = [
            r.incident_weekday,
            r.shift,
            r.console,
            r.supervisor_name,
            goal,
            r.operator,
            r.category_2_incidents_target,
            r.category,
            r.camera_name,
            r.id
        ]
        result_response.append(internal)

    response = {
        'data': data,
        'csv': result_response,
    }
    return jsonify(response)


@api_bp.route('/optimization', methods=['POST'])
@authentication
def edit_optimization(**kwargs):
    json_return = json.loads(os.environ.get("JSON_RESPONSE"))
    data = request.get_json()
    entry_id = data.get('id')
    operator = data.get('operator')
    goal = data.get('goal')
    cat = data.get('category')

    optimization_service = OptimizationService()
    if entry_id is not None:
        confirmation = optimization_service.edit_optimization_cctv(entry_id, operator, goal, cat)
    else:
        confirmation = optimization_service.create_optimization_cctv(data)
    json_return["data"] = confirmation

    return json_return


@api_bp.route('/optimization_report', methods=['POST'])
@authentication
def optimization_report(**kwargs):
    json_return = json.loads(os.environ.get("JSON_RESPONSE"))
    data = request.get_json()
    origin = data.get('origin')
    units = data.get('units')
    operators = data.get('operators')
    supervisors = data.get('supervisors')
    cameras = data.get('cameras')
    dt_start = data.get('dt_start')
    dt_end = data.get('dt_end')

    optimization_service = OptimizationService()
    confirmation = optimization_service.report(origin, units, operators, supervisors, cameras, dt_start, dt_end)
    json_return["data"] = confirmation

    return json_return


@api_bp.route('/camera_information', methods=['GET'])
@use_args(OptimizationSerializer)
@authentication
def get_camera_info(args, **kwargs):
    origin = args.get("origin")
    # unit = args.get("unit")
    manager = args.get("manager")
    # supervisor = args.get("supervisor_name")
    operator = args.get("operator")

    camera_id = args.get("camera_id")
    shift = args.get("shift")
    weekday = args.get("incident_weekday")

    sql = """
                SELECT category_2 as category, camera_id, o.category_2_incidents_target, concat(o.operators_id, ': ', op.name) as operator, o.id, location 
                FROM datalake_ct.otimization_cctv o
                INNER JOIN datalake_ct.cctv_consoles c on (c.id_camera = o.cameras_id)
                INNER JOIN datalake_ct.operator op on (op.id = o.operators_id::text)
                INNER JOIN datalake_ct.cctv_cameras cam on (cam.cam_id = o.cameras_id) 
                --WHERE c.id_camera=split_part(o.camera_id,':',1)
              """
    sql = sql + " AND UPPER(supervisor_name) LIKE '%{}%' ".format(manager) if manager else sql
    # sql = sql + " AND supervisor_name LIKE '%{}%' ".format(supervisor) if supervisor else sql
    sql = sql + " AND operator LIKE '%{}%' ".format(operator) if operator else sql
    # sql = sql + " AND category_2 LIKE '%{}%' ".format(category) if category else sql
    sql = sql + " AND camera_id LIKE '%{}%' ".format(camera_id) if camera_id else sql
    sql = sql + " AND incident_weekday LIKE '%{}%' ".format(weekday) if weekday else sql

    turnos_sql = ''
    if (shift):
        turnos = shift.split('-')
        for t in turnos:
            item = "'{}',".format(t)
            turnos_sql += item
        turnos_sql = turnos_sql[:-1]
        turnos_sql = " AND shift in ({})".format(turnos_sql)
    sql = sql + turnos_sql if shift else sql

    sql = sql + " GROUP BY 1, 2, 3, 4, 5, 6"

    print(sql)
    result = db.session.execute(sql).fetchone()

    data = {
        "category": "--",
        "camera_id": "--",
        "goal": "--",
        "id": "--",
        "camera_location": "--"
    }

    if (result):
        data = {
            "category": result[0],
            "camera_id": result[1],
            "goal": result[2],
            "id": result[4],
            "camera_location": result[5]
        }

    return jsonify(data)
