def sunburst_2(data, result, key, param):
    pass
    for r in result:
        if r[param] == key:
            pass

    data = {
        "name": {0},
        "value": 0,
        "itemStyle": {
            "color": '#da0d68'
        },
        "label": {"color": "#000"},
        "textStyle": {"color": "#000"},
        "children": []
    }


def sunburst(title, result):
    series = []
    data = {
        "name": {0},
        "value": 0,
        "itemStyle": {
            "color": '#da0d68'
        },
        "label": {"color": "#000"},
        "textStyle": {"color": "#000"},
        "children": []
    }

    a = {
        "title": {
            "title": 'Tipo de Ocorrência (%)',
            "subtext": '',
            "left": 'center',
            "textStyle": {
                "fontSize": 16,
                "align": 'center',
                "color": '#52FFEE'
            },
            "subtextStyle": {
                "align": 'center'
            },
        },
        "textStyle": {
            "color": '#FFF'
        },
        "itemStyle": {
            "color": '#FFF'
        },
        "series": {
            "type": 'sunburst',
            "data": []
        },
        "visualMap": {
            "type": 'continuous',
            "min": 0,
            "max": 25,
            "inRange": {
                "color": ['#2F93C8', '#AEC48F', '#FFDB5C', '#F98862']
            },
            "text": ['Alto', 'Baixo'],
            "textStyle": {
                "color": "#FFF"
            }
        }
    }


def choose_chart(tipo, chart_name, result):
    if tipo == 'sunburst':
        result_dict = {}
        for r in result:
            return True
        sunburst(chart_name, result)
