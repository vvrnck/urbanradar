from flask import jsonify
from webargs.flaskparser import use_args
from ext import db
from app.serializers import *
from app.util.decorators import authentication
from flask import Blueprint

api_bp = Blueprint('api', __name__, url_prefix='/api/v1/')


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
