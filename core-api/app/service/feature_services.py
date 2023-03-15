from app.models import *
from app.util_services import generate_chart_options, generate_prediction_icon
from app.model.Field import Field
from app.model.Feature import Feature
from app.model.Properties import Properties
from app.model.Group import Group
from sqlalchemy import func, between, desc, and_
from sqlalchemy.orm import aliased
from datetime import timedelta, datetime
from random import randint
import json


def filter_new(origin, id_layer, dt_start, dt_end, list_ids_cat_arr, hexcode, list_ids_cat_str):
    filters_json = {}
    is_geojson = False
    dt_start_txt = dt_start.strftime("%Y-%m-%d %H:%M:%S")
    dt_end_txt = dt_end.strftime("%Y-%m-%d 23:59:59")
    if id_layer in [49, 52, 53]:
        dt_end = dt_end + timedelta(days=6)
        dt_end_txt = dt_end.strftime("%Y-%m-%d 23:59:59")
    groups = Group.query.filter(Group.origin == origin).order_by(Group.id).all()
    resp = db.session.query(func.cast(func.sum(Properties.value), db.Integer).label("total"),
                            Feature.id.label("id_feature"), Feature.geo_txt,
                            Category.id.label("id_cat"), Feature.code, Category.name.label("category"),
                            Group.type.label("groupname")).outerjoin(Category,
                                                                     Category.id == Properties.id_category).outerjoin(
        Group, Group.id == Category.id_group).join(Feature, Feature.id == Properties.id_feature).filter(
        Feature.id_layer == id_layer).filter(between(func.DATE(Properties.dt_filter), dt_start_txt, dt_end_txt)).filter(
        Feature.code == hexcode).group_by(Feature.id, Feature.code, Feature.geo_txt, Category.id, Category.name,
                                          Group.type).order_by(Feature.id.desc(), desc("total"))

    list_ids_cat = list_ids_cat_str.split("-") if list_ids_cat_str else []
    if list_ids_cat_arr[0]:
        feat_id_list = db.session.query(Properties.id_feature.distinct()).join(Feature,
                                                                               Feature.id == Properties.id_feature).filter(
            between(Properties.dt_filter, dt_start_txt, dt_end_txt)).filter(
            Properties.id_category.in_(list_ids_cat_arr[0])).filter(Feature.code == hexcode)
        for id_cat in list_ids_cat_arr[1:]:
            if id_cat:
                tmp = aliased(Properties)
                feat_id_list = feat_id_list.join(tmp, and_(tmp.id_category.in_(id_cat),
                                                           Properties.id_feature == tmp.id_feature)).filter(
                    between(tmp.dt_filter, dt_start_txt, dt_end_txt))
        feat_id_list = feat_id_list.all()
        resp = resp.filter(Feature.id.in_(feat_id_list))
    resp = resp.all()
    cam_list = []
    features = []

    categories = {}
    for gr in groups:
        categories[str(gr.type)] = []
    categories['popup'] = True
    categories['total'] = 0
    max_total = 0
    min_total = None
    total = ''
    filters = []
    processed_features = []
    cat_copied = categories.copy()
    for r in resp:
        max_total = max(int(r.total), max_total)
        min_total = min(int(r.total), min_total) if min_total is not None else r.total
        if r.id_feature not in processed_features:
            cat_copied = categories.copy()
            if "FeatureCollection" in r.geo_txt:
                is_geojson = True
                feature = {
                    "type": "Feature",
                    "properties": {
                        "id": r.id_feature,
                        "code": r.code
                    },
                    "geometry": r.geo_txt
                }

            else:
                feature = {
                    "id": r.id_feature,
                    "name": r.code,
                    "type": "polygon",
                    "coords": json.loads(r.geo_txt),
                }
            features.append({**feature, "properties": cat_copied})
            processed_features.append(r.id_feature)
        if total == '' and r.groupname:
            total = r.groupname
        if r.groupname and r.groupname == total:
            cat_copied["Total"] = cat_copied.get("Total", 0) + int(r.total)

        if r.groupname and len(cat_copied[r.groupname]) < 5:
            cat_copied[r.groupname].append({
                "value": int(r.total),
                "name": r.category,
            })

        if list_ids_cat:
            for idc in list_ids_cat:
                if r.id_cat == int(idc):
                    filters.append({
                        "value": int(r.total),
                        "name": r.category
                    })

    if is_geojson:
        result = {
            "id": id_layer,
            "features": {
                "type": "FeatureCollection",
                "features": features,
                "rangeTotal": [min_total, max_total],
                "filters": filters
            }
        }
    else:
        result = {
            "id": id_layer,
            "features": features,
            "rangeTotal": [min_total, max_total],
            "filters": filters
        }
    result["cam_list"] = cam_list

    intervalos = [
        ("22:00:00", "23:59:59"),
        ("20:00:00", "21:59:59"),
        ("18:00:00", "19:59:59"),
        ("16:00:00", "17:59:59"),
        ("14:00:00", "15:59:59"),
        ("12:00:00", "13:59:59"),
        ("10:00:00", "11:59:59"),
        ("08:00:00", "09:59:59"),
        ("06:00:00", "07:59:59"),
        ("04:00:00", "05:59:59"),
        ("02:00:00", "03:59:59"),
        ("00:00:00", "01:59:59"),
    ]
    heatmap_intervals = intervalos.copy()
    y_index = ""
    x_index = ""
    chart_queries = db.session.query(GenericQueries.query_sql, GenericQueries.query_key, GenericQueries.filters,
                                     GenericQueries.layers).filter(
        GenericQueries.origin == origin).filter(GenericQueries.type_ == "features").all()
    if origin == "SC":
        if id_layer == 35:
            x_index, y_index, a, b, c = hexcode.split("_")
        else:
            x_index, y_index = hexcode.split("_")
        x_index += ".0"
        y_index += ".0"
    result["charts"] = []

    dt_start_graph = dt_start
    for chart_query in chart_queries:
        if chart_query.layers is None:
            continue
        if id_layer not in chart_query.layers:
            continue
        type_ = ""
        name = ""
        heatmap_series = []
        serie_list = None
        filters = []
        timed_filters = []
        c = []

        for id_ in list_ids_cat:
            category = db.session.query(Category).join(Group).add_column(Group.type). \
                filter(Category.id == id_).first()
            c.append(category)
        for f in chart_query.filters:
            filter_in = []
            time_filter = []
            for category in c:
                if category.type == 'Category CCTV' and f == 'cctv.\"Category 1\"':
                    filter_in.append(category.Category.name)
                if category.type == 'Responded To By' and f == 'cctv.\"Responded To By\"':
                    filter_in.append(category.Category.name)
                if category.type == 'Setores' and f == 'hexsetores.id_setor':
                    pass
                if category.type == 'Tipo de Ocorrência' and f == 'atd.tipo_ocorrencia':
                    filter_in.append(category.Category.name)
                if category.type == 'Atividade' and f == 'desl.atividade':
                    filter_in.append(category.Category.name)
                if category.type == 'Guarnição' and f == 'desl.guarnicao':
                    filter_in.append(category.Category.name)
                if category.type == 'Turno' and f == 'desl.hora_desloc':
                    time_filter.append(category.Category.name)
                    if len(intervalos) == 12:
                        intervalos.clear()
                    intervalo = category.Category.name.split(" - ")
                    intervalo_tuple = (intervalo[0], intervalo[1])
                    intervalos.append(intervalo_tuple) if intervalo_tuple not in intervalos else intervalos
                if category.type == 'Turno - 2h' and f == 'atd.hora_fato':
                    time_filter.append(category.Category.name)
                    if len(intervalos) == 12:
                        intervalos.clear()
                    intervalo = category.Category.name.split(" - ")
                    intervalo_tuple = (intervalo[0], intervalo[1])
                    intervalos.append(intervalo_tuple) if intervalo_tuple not in intervalos else intervalos
                if category.type == 'Shift' and f == 'to_timestamp(cctv.\"Incident Time\", \'HH24:MI:SS\')::time':
                    time_filter.append(category.Category.name)
                    if len(intervalos) == 12:
                        intervalos.clear()
                    intervalo = category.Category.name.split(" - ")
                    intervalo_tuple = (intervalo[0], intervalo[1])
                    intervalos.append(intervalo_tuple) if intervalo_tuple not in intervalos else intervalos
            if "id_category" in f and list_ids_cat:
                filters.append("{} in ({})".format(f, list_ids_cat_str.replace('-', ',', len(list_ids_cat))))
            if filter_in:
                aux = []
                for param in filter_in:
                    if type(param) == int:
                        aux.append('LOWER(\'' + str(param) + '\')')
                    else:
                        aux.append('LOWER(\'' + param + '\')')
                auxstr = ','.join(aux)
                filters.append("LOWER({}) in ({})".format(f, auxstr))
            if time_filter:
                aux = []
                timed_filters.clear()
                for intervalo in intervalos:
                    aux.append('{0} BETWEEN \'{1}\' AND \'{2}\''.format(f, intervalo[0], intervalo[1]))
                auxstr = ' OR '.join(aux)
                timed_filters.append("( {} )".format(auxstr))

        filters_joined = " and {}".format(" and ".join(filters)) if filters else ""
        all_filters_joined = filters_joined + (" and {}".format(" and ".join(timed_filters)) if timed_filters else "")
        if "heatmap_feature" in chart_query.query_key:
            save_one = None
            for intervalo in intervalos:
                count_array = []
                heatmap_formatted = chart_query.query_sql.format(intervalo[0], intervalo[1],
                                                                 x_index if x_index and "index" in chart_query.query_key else hexcode,
                                                                 y_index, dt_start_graph, dt_end, filters_joined,
                                                                 id_layer)
                print({"Query": heatmap_formatted})
                serie_list = db.session.execute(heatmap_formatted).fetchall()
                if not serie_list:
                    continue
                else:
                    save_one = serie_list.copy()
                for s in serie_list:
                    count_value = s[3]
                    while len(count_array) != s[2]:
                        count_array.append(0)
                    count_array.append(count_value)
                serie_obj = {
                    "name": intervalo[0] + ' - ' + intervalo[1],
                    "data": count_array
                }
                heatmap_series.append(serie_obj)
            serie_list = save_one if save_one else serie_list
        elif "heatmap_cctv" in chart_query.query_key:
            heatmap_formatted = chart_query.query_sql.format(None, None,
                                                             x_index if x_index and "index" in chart_query.query_key else hexcode,
                                                             y_index, dt_start_graph, dt_end, filters_joined, id_layer)
            print({"Query": heatmap_formatted})
            serie_list = db.session.execute(heatmap_formatted).fetchall()
            keys = []
            for s in serie_list:
                if s[3] not in keys:
                    keys.append(s[3])
            for key in keys:
                data = []
                for i in range(0, 6):
                    day = dt_start_graph + timedelta(days=i)
                    aux = {}
                    for si in serie_list:
                        current = datetime.strptime(si[2], '%Y-%m-%d').date()
                        if si[3] == key and str(day) == str(current):
                            aux = {"x": si[2], "y": si[4]}
                            data.append(aux)
                    if aux == {}:
                        aux = {"x": str(day), "y": 'not-found' }
                        data.append(aux)
                ret = {"name": key, "data": data}
                heatmap_series.append(ret)
        else:
            chart_formatted = chart_query.query_sql.format(
                x_index if x_index and "index" in chart_query.query_key else hexcode, y_index, dt_start_graph, dt_end,
                id_layer, all_filters_joined)
            serie_list = db.session.execute(chart_formatted).fetchall()
            print("Serie List : " + str(len(serie_list)))
            print({"Query": chart_formatted})
        if serie_list:
            name = serie_list[0][0]
            type_ = serie_list[0][1]
        chart_options, series = generate_chart_options(type_, name, serie_list, intervalos=heatmap_intervals,
                                                       name_position=2,
                                                       value_position=3)
        series = heatmap_series if heatmap_series else series
        result["charts"].append({"chart_options": chart_options, "series": series})
    return result


def filter2(origin, id_layer, dt_start, dt_end, list_ids_cat_str, id_cat_sep_arr_sql):  # Bring all hexs to plot on map
    dt_start_txt = dt_start.strftime("%Y-%m-%d %H:%M:%S")
    dt_end_txt = dt_end.strftime("%Y-%m-%d 23:59:59")

    if id_layer not in [49, 52, 53]:
        sql = """
            SELECT f.id as id_feature,
                f.code as code,
                f.geo_txt as geo_txt,
                c.name as category,
                cast(sum(p.value) as Integer) as total,
                f.style as style,
                g.type as group
            FROM web.properties p
                LEFT JOIN web.category c on p.id_category = c.id
                JOIN web.feature f ON p.id_feature = f.id
                LEFT JOIN web.group g on g.id = c.id_group
            WHERE f.id_layer = {id_layer}
                AND f.origin = '{origin}'
                AND p.dt_filter between '{dt_start_txt}' AND '{dt_end_txt}'
        """
    else:
        sql = """
            SELECT f.id as id_feature,
                f.code as code,
                f.geo_txt as geo_txt,
                c.name as category,
                cast(sum(p.value) as Integer) as total,
                f.style as style,
                g.type as group,
                pt.tipo_atendimento as classificacao_atendimento,
                pt.tipo_atendimento,
	            replace((replace(RPAD(prob_ocorrencia::text,2,'0'),',','.')::numeric/10 * max(gravidade::numeric))::text, '.', ',') as prob_ocorrencia
            FROM web.properties p
                LEFT JOIN web.category c on p.id_category = c.id
                JOIN web.feature f ON p.id_feature = f.id
                LEFT JOIN web.group g on g.id = c.id_group
                INNER JOIN datalake_sc."Prediction_Association" pt on pt.hexagono = f.code
                INNER JOIN datalake_sc.ocorrencia_gravidade on pt.tipo_atendimento = ocorrencia_gravidade.tipo_de_ocorrencia
            WHERE f.id_layer = {id_layer}
                AND f.origin = '{origin}'
                AND pt.data_ocorrencia between SPLIT_PART('{dt_start_txt}', ' ', 1) AND SPLIT_PART('{dt_end_txt}', ' ', 1)
        """

    sql = sql.format(
        id_layer=id_layer,
        origin=origin,
        dt_start_txt=dt_start_txt,
        dt_end_txt=dt_end_txt
    )
    list_ids_cat = list_ids_cat_str.split("-") if list_ids_cat_str else []
    if id_cat_sep_arr_sql[0]:
        ids_cats = ''

        sql2 = "select p1.id_feature from web.properties p1"
        sql_where = ""
        for i in range(len(id_cat_sep_arr_sql)):
            if id_cat_sep_arr_sql[i]:
                if i == 0:
                    sql_where = " where "
                    sql_where += " p{}.id_category in  {}  ".format(i + 1, id_cat_sep_arr_sql[0])
                    sql_where += " AND p{}.dt_filter between '{}' AND '{}'".format(i + 1, dt_start_txt, dt_end_txt)
                else:
                    sql2 += " inner join web.properties p{} on p{}.id_feature = p{}.id_feature and p{}.id_category in  {} ".format(
                        i + 1, i, i + 1, i + 1, id_cat_sep_arr_sql[i])
                    sql2 += " AND p{}.dt_filter between '{}' AND '{}'".format(i + 1, dt_start_txt, dt_end_txt)

        sql2 += sql_where
        sql2 += ' GROUP BY p1.id_feature'
        cursor = db.session.execute(sql2)

        r = cursor.fetchall()

        if len(r) > 0:
            ids_cats = str(r).replace('(', '').replace(',),', ',').replace(')', '').replace(',]', '').replace('[',
                                                                                                              '')
            sql += ' AND f.id in ({})'.format(ids_cats)
        else:
            sql += ' AND f.id in (0)'

        cursor.close()
    if list_ids_cat:
        sql += ' AND c.id in {} '.format(id_cat_sep_arr_sql[0])
    sql += ' GROUP BY f.id, f.code, f.geo_txt, c.name, f.style, g.type ORDER BY f.id, total DESC' if id_layer not in [49, 52, 53] else ' GROUP BY f.id, f.code, f.geo_txt, c.name, f.style, g.type, pt.prob_ocorrencia, pt.tipo_atendimento ORDER BY f.id, total DESC'

    print({"Query": sql})
    print(sql)

    cursor = db.session.execute(sql)

    features = []

    is_geojson = False
    i = 0
    id_feature = 0
    maxTotal = 0
    minTotal = 0
    firstLoop = True

    while True:
        r = cursor.fetchone()

        if r and r["total"] and type(r["total"]) == int:
            if firstLoop:
                maxTotal = r["total"]
                minTotal = r["total"]
                firstLoop = False
            else:
                if r["total"] > maxTotal:
                    maxTotal = r["total"]
                if r["total"] < minTotal:
                    minTotal = r["total"]

        if not r:
            if id_feature != 0:
                features.append({**feature})
            break
        i = i + 1
        if id_feature != r['id_feature']:
            if id_feature != 0:
                features.append({**feature})

            id_feature = r['id_feature']
            if "FeatureCollection" in r['geo_txt']:
                is_geojson = True
                feature = {
                    "type": "Feature",
                    "properties": {
                        "id": r["id_feature"],
                        "code": r["code"],
                        "Total": r["total"]
                    },
                    "geometry": r["geo_txt"]
                }

            else:
                if len(json.loads(r["geo_txt"])) == 3:
                    if r["style"] != None:
                        if r['group'] == 'Atividade':
                            feature = {
                                "id": r["id_feature"],
                                "name": r["code"],
                                "type": "circle",
                                "coords": json.loads(r["geo_txt"]),
                                "Total": r["total"],
                                "style": json.loads(r["style"]),
                                "category": r["category"]
                            }
                        else:
                            feature = {
                                "id": r["id_feature"],
                                "name": r["code"],
                                "type": "circle",
                                "coords": json.loads(r["geo_txt"]),
                                "Total": r["total"],
                                "style": json.loads(r["style"]),
                            }
                    else:
                        feature = {
                            "id": r["id_feature"],
                            "name": r["code"],
                            "type": "circle",
                            "coords": json.loads(r["geo_txt"]),
                            "Total": r["total"],
                            "style": False
                        }

                else:
                    feature = {
                        "id": r["id_feature"],
                        "name": r["code"],
                        "type": "polygon",
                        "coords": json.loads(r["geo_txt"]),
                        "Total": r["total"]
                    }
                    if id_layer in [49, 52, 53]:
                        name = r['tipo_atendimento']
                        prob = r['prob_ocorrencia']
                        feature.update({"prediction": generate_prediction_icon(name, str(prob))})
    if is_geojson:
        result = {
            "id": id_layer,
            "features": {
                "type": "FeatureCollection",
                "rangeTotal": [minTotal, maxTotal]
            }
        }
    else:
        result = {
            "id": id_layer,
            "features": features,
            "rangeTotal": [minTotal, maxTotal]
        }

    return result
