from pip._vendor.packaging.markers import Op

from app.model.Cctv import OptimizationCCTV, CCTVConsoles, RawCCTV
from ext import db
from sqlalchemy import func as fn
from datetime import datetime


class OptimizationService:

    @staticmethod
    def list_optimization_cctv():
        pass

    @staticmethod
    def edit_optimization_cctv(entry_id, operator, goal, category):
        optimization_entry = OptimizationCCTV.query.filter(OptimizationCCTV.id == entry_id).first()

        optimization_entry.operators_id = operator
        optimization_entry.category_2_incidents_target = goal
        optimization_entry.category_2 = category
        optimization_entry.is_edited = True

        db.session.commit()

        optimization_json = {"id": optimization_entry.id, "operator": optimization_entry.operators_id,
                             "goal": optimization_entry.category_2_incidents_target, "category": optimization_entry.category_2}

        return optimization_json

    @staticmethod
    def list_optimization_calendar(org, unit, supervisor, operator,
                                   cat2, camera_location, camera_id, shift):
        optimization_query = OptimizationCCTV.query.filter(OptimizationCCTV.cctv_unit == unit)
        if supervisor:
            optimization_query.filter(OptimizationCCTV.supervisor_name.in_(supervisor))
        if operator:
            optimization_query.filter(OptimizationCCTV.operator.in_(operator))
        if cat2:
            optimization_query.filter(OptimizationCCTV.category_2.in_(cat2))
        if shift:
            optimization_query.filter(OptimizationCCTV.supervisor_name.in_(shift))
        pass

    def report(self, origin, units, operators, supervisors, cameras, dt_start, dt_end):
        # Create optimization query
        optimization_date_replaced = fn.to_timestamp(fn.replace(OptimizationCCTV.optm_date, '.', '-'), 'DD-MM-YYYY')
        base_optimization_query = OptimizationCCTV.query.with_entities(fn.count(OptimizationCCTV.cameras_persona_category_2),
                                                                       OptimizationCCTV.optm_date)
        base_optimization_query = base_optimization_query.filter(optimization_date_replaced.between(dt_start, dt_end))

        # Create events query
        cctv_date_replaced = fn.to_timestamp(fn.replace(RawCCTV.incident_date, '.', '-'), 'DD-MM-YYYY')
        base_cctv_incidents = RawCCTV.query.with_entities(fn.count(RawCCTV.reference),
                                                          RawCCTV.incident_date)

        base_cctv_incidents = base_cctv_incidents.filter(cctv_date_replaced.between(dt_start, dt_end))

        if not units:
            raise KeyError("Units not provided")
        for unit in units:
            if unit == 'Capetown':
                base_optimization_query = base_optimization_query.filter(OptimizationCCTV.cctv_unit == 'CAPE TOWN')
                base_cctv_incidents = base_cctv_incidents.filter(RawCCTV.cctv_unit == 'Cape Town')
            elif unit == 'Goodwood':
                base_optimization_query = base_optimization_query.filter(OptimizationCCTV.cctv_unit == 'GOODWOOD')
                base_cctv_incidents = base_cctv_incidents.filter(RawCCTV.cctv_unit == 'Goodwood')

        if operators:
            base_optimization_query = base_optimization_query.filter(OptimizationCCTV.operator.in_(operators))
            base_cctv_incidents = base_cctv_incidents.filter(RawCCTV.operator.in_(operators))
        if supervisors:
            base_optimization_query = base_optimization_query.filter(OptimizationCCTV.operator.in_(supervisors))
            base_cctv_incidents = base_cctv_incidents.filter(RawCCTV.supervisor_name.in_(supervisors))
        #if cameras:
         #   base_optimization_query = base_optimization_query.filter(OptimizationCCTV.camera_id.in_(cameras))
          #  base_cctv_incidents = base_cctv_incidents.filter(RawCCTV.camera_location.in_(cameras))

        base_optimization_query = base_optimization_query.group_by(OptimizationCCTV.optm_date)
        base_cctv_incidents = base_cctv_incidents.group_by(RawCCTV.incident_date)

        optimization_results = base_optimization_query.order_by(OptimizationCCTV.optm_date).all()
        past_incidents_results = base_cctv_incidents.order_by(RawCCTV.incident_date).all()

        series = []
        categories = []

        # Assemble returns here
        # [(19, '25.08.2020'), (4, '26.08.2020'), (8, '27.08.2020'), (4, '28.08.2020'), (188, '29.08.2020'), (10, '30.08.2020'), (8, '31.08.2020')]

        optimization_json = {"name": "Optimization", "data": []}
        real_json = {"name": "Real", "data": []}

        for opt in optimization_results:
            optimization_json.get("data").append(opt[0])
            fixed_date = ''
            try:
                fixed_date = str(datetime.strptime(opt[1], '%d.%m.%Y').date())
                categories.append(fixed_date) if fixed_date not in categories else categories
            except Exception as err:
                print("Error trying to convert date into strptime in Optimization Service.")

        for past in past_incidents_results:
            real_json.get("data").append(past[0])
            fixed_date = ''
            try:
                fixed_date = str(datetime.strptime(past[1], '%d.%m.%Y').date())
                categories.append(fixed_date) if fixed_date not in categories else categories
            except Exception as err:
                print("Error trying to convert date into strptime in Optimization Service.")

        series.append(optimization_json)
        series.append(real_json)
        return_json = self.report_chart_options(categories)

        chart_json = {"series": series, "chartOptions": return_json}

        return chart_json

    @staticmethod
    def report_chart_options(categories):
        return {
            "chart": {
              'type': 'bar',
              'height': 350,
              'stacked': True,
              'foreColor': '#FFF',
              'toolbar': {
                'show': True
              },
              'zoom': {
                'enabled': True
              }
            },
            'responsive': [{
              'breakpoint': 480,
              'options': {
                'legend': {
                  'position': 'bottom',
                  'offsetX': -10,
                  'offsetY': 0
                }
              }
            }],
            'plotOptions': {
              'bar': {
                'borderRadius': 8,
                'horizontal': False,
              },
            },
            'xaxis': {
              'type': 'datetime',
              'categories': categories,
            },
            'legend': {
              'position': 'right',
              'offsetY': 40
            },
            'fill': {
              'opacity': 1
            }
        }
