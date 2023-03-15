import copy


def generate_chart_options(chart_type, chart_name, serie, intervalos, name_position, value_position):
    chart_options = {
        "xaxis": {
            "type": None,
            "categories": [],
            "labels": {
                "style": {
                    "colors": [],
                }
            }
        },
        "yaxis": {
            "labels": {
                "style": {
                    "colors": [],
                }
            }
        },
        "chart": {
            "height": 350,
            "type": None
        },
        "dataLabels": {
            "enabled": "false",
        },
        "title": {
            "text": None,
            "align": "center",
            "style": {
                "color": "#FFFFFF"
            }
        }
    }
    series = []
    if chart_type.strip() == "area":
        chart_options["title"]["text"] = chart_name
        chart_options["chart"]["type"] = 'area'
        cat = []
        for s in serie:
            cat.append(s[name_position])
            series.append({"name": s[value_position], "data": s[4]})
        chart_options["xaxis"]["categories"] = cat
        chart_options["xaxis"]["type"] = "datetime"
        chart_options["tooltip"] = {"x": {"format": "dd/MM/yy HH:mm"}}
        chart_options["chart"]["foreColor"] = "#FFFFFF"
        chart_options["stroke"] = {"curve": "smooth"}
        series = series

    elif chart_type.strip() == "dynamic_bar":
        from random import randrange
        data = []
        quarters = {}
        chart_options["title"]["text"] = chart_name
        chart_options["chart"]["type"] = chart_type
        for s in serie:
            if s[name_position] in quarters:
                quarters[s[name_position]]["values"].append({"x": s[value_position], "y": s[value_position + 1]})
                quarters[s[name_position]]["total"] += int(s[value_position + 1])
            else:
                quarters[s[name_position]] = {"values": [{"x": s[value_position], "y": s[value_position + 1]}],
                                              "total": int(s[value_position + 1])}
        i = 0
        colors = ['#F7FFFC', '#008FFB', '#00E396', '#FEB019', '#FF4560', '#775DD0', '#00D9E9', '#FF66C3', '#FF6677',
                  '#FF1A33', '#4C070F']
        for q in quarters.keys():
            tmp = {"x": q, "y": int(quarters[q]["total"]), "color": colors[randrange(10)],
                   "quarters": quarters[q]["values"]}
            data.append(tmp)
            i += 1
        series = [{"data": data}]

    elif chart_type.strip() == "dynamic_bar_percentage":
        data = []
        quarters = {}
        daily_prob = {}
        chart_options["title"]["text"] = chart_name
        chart_options["chart"]["type"] = "dynamic_bar"
        for s in serie:
            if s[name_position] in quarters:
                found = False
                for period in quarters[s[name_position]]["values"]:
                    if period["name"] == s[value_position]:
                        a_data = period["data"]
                        daily_prob = {"x": s[value_position + 2], "y": int(s[value_position + 1])}
                        a_data.append(daily_prob)
                        # s[name_position]["values"]["data"] = a_data
                        found = True
                if not found:
                    daily_prob = {"x": s[value_position + 2], "y": int(s[value_position + 1])}
                    quarters[s[name_position]]["values"].append({"name": s[value_position], "data": [daily_prob]})
            else:
                daily_prob = {"x": s[value_position + 2], "y": int(s[value_position + 1])}
                new_data = [daily_prob]
                quarters[s[name_position]] = {"values": [{"name": s[value_position], "data": new_data}],
                                              "total": int(s[value_position + 1])}
        for q in quarters:
            quarters[q]['total'] = int(quarters[q]['total'] / (len(quarters[q]['values'])))
        i = 0
        colors = ['#F7FFFC', '#008FFB', '#00E396', '#FEB019', '#FF4560', '#775DD0', '#00D9E9', '#FF66C3', '#FF6677',
                  '#FF1A33', '#4C070F']
        # 0 - 10 #F7FFFC
        # 10 - 20 #008FFB
        # 20 - 30 #00E396
        # 30 - 40 #FEB019
        # 40 - 50 #FF4560
        # 50 - 60 #775DD0
        # 60 - 70 #00D9E9
        # 70 - 80 #FF66C3
        # 80 - 90 #FF6677
        # 90 - 100 #FF1A33
        for q in quarters.keys():
            try:
                tmp = {"x": q, "y": int(quarters[q]["total"]), "color": colors[int(quarters[q]["total"]/10)],
                       "quarters": quarters[q]["values"]}
            except Exception as err:
                from random import randrange
                tmp = {"x": q, "y": int(quarters[q]["total"]), "color": colors[randrange(10)],
                       "quarters": quarters[q]["values"]}
            data.append(tmp)
            i += 1
        series = [{"data": data}]

    elif chart_type.strip() == "level_chart":
        data = []
        category_one = {"x": "", "y": 0, "count": 0, "quarters": []}
        category_two = {"x": "", "y": 0, "count": 0, "quarters": []}
        quarters_cat_two = {"name": "", "data": []}
        quarters_data = {"x": "", "y": ""}

        quarters = []

        chart_options["title"]["text"] = chart_name
        chart_options["chart"]["type"] = "level_chart"
        for s in serie:
            cat_one = {}
            cat_two = {}
            if any(d['x'] == s[2] for d in quarters):
                for quart in quarters:
                    if quart["x"] == s[2]:
                        cat_one = quart
            else:
                cat_one = copy.deepcopy(category_one)
                cat_one["x"] = s[2]
                quarters.append(cat_one)

            if any(d['x'] == s[3] for d in cat_one['quarters']):
                for quart in cat_one["quarters"]:
                    if quart["x"] == s[3]:
                        cat_two = quart
            else:
                cat_two = copy.deepcopy(category_two)
                cat_two["x"] = s[3]
                cat_one["quarters"].append(cat_two)

            cat_one["y"] = cat_one["y"] + int(s[4])
            cat_two["y"] = cat_two["y"] + int(s[5])  # todo revisar divisoes

            cat_one["count"] = cat_one["count"] + 1
            cat_two["count"] = cat_two["count"] + 1

            if any(d['name'] == s[7] for d in cat_two['quarters']):
                for quart in cat_two["quarters"]:
                    if quart["name"] == s[7]:
                        quart_cat_two = quart
                        for q in quart_cat_two["data"]:
                            if q["x"] == s[6]:
                                q["y"] = s[5]

            else:
                quart_cat_two = copy.deepcopy(quarters_cat_two)
                quart_cat_two["name"] = s[7]
                x_axis = ['madrugada', 'manhã', 'tarde', 'noite']
                for i in range(0, 4):
                    quart_cat_two_data = copy.deepcopy(quarters_data)
                    quart_cat_two_data["x"] = x_axis[i]
                    quart_cat_two_data["y"] = 0
                    quart_cat_two["data"].append(quart_cat_two_data)
                for q in quart_cat_two["data"]:
                    if q["x"] == s[6]:
                        q["y"] = s[5]

                cat_two["quarters"].append(quart_cat_two)

        for quart in quarters:
            quart["y"] = quart["y"]/quart["count"]
            for q in quart["quarters"]:
                q["y"] = q["y"]/q["count"]
        series = [{"data": quarters}]

    elif chart_type.strip() == "donut":
        chart_options["chart"]["type"] = chart_type
        chart_options["chart"]["foreColor"] = "#FFFFFF"
        chart_options["dataLabels"] = {"enabled": True}
        chart_options["title"]["text"] = chart_name
        labels = []
        for s in serie:
            labels.append(s[name_position])
            series.append(s[value_position])
        chart_options["labels"] = labels
        chart_options["plotOptions"] = {"pie": {"donut": {
            "labels": {"show": False, "name": {"show": True, "color": "#FFFFFF"},
                       "value": {"show": True, "color": "#FFFFFF"}}}}}
        chart_options["responsive"] = [
            {"breakpoint": 480, "options": {"chart": {"width": 200}, "legend": {"position": "bottom"}}}]
    elif chart_type.strip() == "bar":
        chart_options["chart"]["type"] = chart_type
        chart_options["chart"]["height"] = 350
        chart_options["title"]["text"] = chart_name
        chart_options["plotOptions"] = {"bar": {"horizontal": True}}
        categories = []
        for s in serie:
            categories.append(s[name_position])
            series.append(s[value_position])
        series = [{"data": series}]
        chart_options["chart"]["foreColor"] = "#FFFFFF"
        chart_options["legend"] = {"show": False}
        chart_options["xaxis"] = {"categories": categories,
                                  "labels": {"style": {"colors": ["#FFFFFF" for i in range(len(series))]}}}
        chart_options["yaxis"] = {"labels": {"style": {"colors": ["#FFFFFF" for i in range(len(categories))]}}}
    elif chart_type.strip() == "heatmap":
        chart_options["xaxis"]["type"] = "Week Days"
        chart_options["xaxis"]["categories"] = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
                                                "Saturday"]
        chart_options["colors"] = ["#B71C1C"]
        chart_options["plotOptions"] = {
            "heatmap": {"colorScale": {"ranges": [{"from": -100, "to": 0, "color": '#484848'}]}}}
        chart_options["legend"] = {"show": False}
        chart_options["chart"]["type"] = chart_type
        chart_options["yaxis"]["labels"]["style"]["colors"] = ["#FFFFFF" for i in range(len(intervalos))]
        chart_options["xaxis"]["labels"]["style"]["colors"] = ["#FFFFFF" for i in range(7)]
        chart_options["title"]["text"] = chart_name
    elif chart_type.strip() == "custom_heatmap":
        chart_options["plotOptions"] = {
            "heatmap": {"enableShades": False, "colorScale": {"ranges": [{"from": 100, "to": 110, "color": '#D3D3D3'},
                                                                         {"from": 0, "to": 9, "color": '#00007F'},
                                                                         {"from": 10, "to": 19, "color": '#0000FF'},
                                                                         {"from": 20, "to": 29, "color": '#007FFF'},
                                                                         {"from": 30, "to": 39, "color": '#00FFFF'},
                                                                         {"from": 40, "to": 49, "color": '#7FFF7F'},
                                                                         {"from": 50, "to": 59, "color": '#FFFF00'},
                                                                         {"from": 60, "to": 69, "color": '#FF7F00'},
                                                                         {"from": 70, "to": 79, "color": '#B35900'},
                                                                         {"from": 80, "to": 89, "color": '#FF0000'},
                                                                         {"from": 90, "to": 99, "color": '#7F0000'}, ]}}
        }
        chart_options["chart"]["type"] = chart_type
        chart_options["title"]["text"] = chart_name
        chart_options["dataLabels"] = {"enabled": True}
        chart_options["chart"]["foreColor"] = "#FFF"
        chart_options.pop('xaxis')
        chart_options.pop('yaxis')
    elif chart_type.strip() == "line":
        linechart_count_array = []
        linechart_mes_ano_array = []
        chart_options["chart"]["type"] = chart_type
        chart_options["dataLabels"] = {"enabled": True}

        if "colors" in chart_options:
            chart_options.pop("colors")
        for s in serie:
            mes_ano = s[name_position]
            count_value = s[value_position]
            linechart_count_array.append(count_value)
            linechart_mes_ano_array.append(mes_ano)

        serie_obj = {
            "name": "Incidentes",
            "data": linechart_count_array,
        }

        series.append(serie_obj)

        chart_options["xaxis"]["type"] = chart_type
        chart_options["chart"]["zoom"] = {"enabled": True}
        chart_options["xaxis"]["categories"] = linechart_mes_ano_array
        chart_options["yaxis"]["labels"]["style"]["colors"] = ["#FFFFFF" for i in range(len(linechart_count_array))]
        chart_options["xaxis"]["labels"]["style"]["colors"] = ["#FFFFFF" for i in range(len(linechart_mes_ano_array))]
        chart_options["title"]["text"] = chart_name
        chart_options["stroke"] = {"curve": "straight"}
        chart_options["grid"] = {"row": {"colors": ['#f3f3f3', 'transparent'], "opacity": 0.5}}
    return chart_options, series


def generate_prediction_icon(name, prob):
    try:
        prob = float(prob.replace(',', '.'))
    except Exception as err:
        print(err)
        return {"name": name, "type": "invalido", "amount": 0, "color": '#098765'}
    if "Acidente" in name:
        return {"name": name, "type": "acidente", "amount": 0, "color": getHexColor(prob)}

    elif name == "Acidente de trânsito (Com pessoa ferida ou morta)":
        return {"name": name, "type": "acidente", "amount": 0, "color": getHexColor(prob)}

    elif name == "Acidente de trânsito (Apenas danos materiais)":
        return {"name": name, "type": "acidente", "amount": 0, "color": getHexColor(prob)}

    elif name == "Afastar-se o condutor do veículo do local do acidente, para fugir à responsabilidade":
        return {"name": name, "type": "invalido", "amount": 0, "color": getHexColor(prob)}

    elif name == "Ameaça":
        return {"name": name, "type": "invalido", "amount": 0, "color": getHexColor(prob)}

    elif name == "Apoio a instituições privadas":
        return {"name": name, "type": "invalido", "amount": 0, "color": getHexColor(prob)}

    elif name == "Apoio a órgãos da administração pública":
        return {"name": name, "type": "invalido", "amount": 0, "color": getHexColor(prob)}

    elif name == "Apoio ao poder judiciário":
        return {"name": name, "type": "invalido", "amount": 0, "color": getHexColor(prob)}

    elif name == "Apoio aos órgãos de segurança pública":
        return {"name": name, "type": "invalido", "amount": 0, "color": getHexColor(prob)}

    elif name == "Ato obsceno":
        return {"name": name, "type": "invalido", "amount": 0, "color": getHexColor(prob)}

    elif name == "Auxílio a comunidade ou pessoa com problema de saúde":
        return {"name": name, "type": "invalido", "amount": 0, "color": getHexColor(prob)}

    elif name == "Averiguação de veículo suspeito":
        return {"name": name, "type": "invalido", "amount": 0, "color": getHexColor(prob)}

    elif name == "Alarme":
        return {"name": name, "type": "alarme", "amount": 0, "color": getHexColor(prob)}

    elif name == "Arma de fogo":
        return {"name": name, "type": "arma_de_fogo", "amount": 0, "color": getHexColor(prob)}

    elif name == "Auxílio a comunidade ou pessoa com problema de saúde ":
        return {"name": name, "type": "auxilio_apoio", "amount": 0, "color": getHexColor(prob)}

    elif name == "Averiguação de pessoa em atitude suspeita":
        return {"name": name, "type": "averiguacao_pessoa_atitude_suspeita", "amount": 0, "color": getHexColor(prob)}

    elif name == "Bomba":
        return {"name": name, "type": "bomba", "amount": 0, "color": getHexColor(prob)}

    elif name == "Busca salvamento":
        return {"name": name, "type": "busca_salvamento", "amount": 0, "color": getHexColor(prob)}

    elif name == "Corromper ou facilitar a corrupção de menor de 18 anos, com ele praticando infração penal ou induzindo-o a praticá-la":
        return {"name": name, "type": "invalido", "amount": 0, "color": getHexColor(prob)}

    elif name == "Cumprimento de Mandado de Prisão/Apreensão de Adolescente":
        return {"name": name, "type": "invalido", "amount": 0, "color": getHexColor(prob)}

    elif name == "Conflito de trânsito":
        return {"name": name, "type": "conflito_transito", "amount": 0, "color": getHexColor(prob)}

    elif name == "Consumidor sade":
        return {"name": name, "type": "consumidor_sade", "amount": 0, "color": getHexColor(prob)}

    elif name == "Contra a pessoa":
        return {"name": name, "type": "contra_a_pessoa", "amount": 0, "color": getHexColor(prob)}

    elif name == "Contra a vida":
        return {"name": name, "type": "contra_a_vida", "amount": 0, "color": getHexColor(prob)}

    elif name == "Crime de trânsito":
        return {"name": name, "type": "crime_de_transito", "amount": 0, "color": getHexColor(prob)}

    elif name == "Dano":
        return {"name": name, "type": "dano", "amount": 0, "color": getHexColor(prob)}

    elif name == "Desacordo comercial":
        return {"name": name, "type": "invalido", "amount": 0, "color": getHexColor(prob)}

    elif name == "Defesa do consumidor":
        return {"name": name, "type": "defesa_do_consumidor", "amount": 0, "color": getHexColor(prob)}

    elif name == "Desastre natural":
        return {"name": name, "type": "desatre natural", "amount": 0, "color": getHexColor(prob)}

    elif name == "Desordem":
        return {"name": name, "type": "desordem", "amount": 0, "color": getHexColor(prob)}

    elif name == "Desordem sade":
        return {"name": name, "type": "desordem_sade", "amount": 0, "color": getHexColor(prob)}

    elif name == "Difamação":
        return {"name": name, "type": "contra_a_pessoa", "amount": 0, "color": getHexColor(prob)}

    elif name == "Dignidade sexual":
        return {"name": name, "type": "dignidade_sexual", "amount": 0, "color": getHexColor(prob)}

    elif name == "Drogas":
        return {"name": name, "type": "drogas", "amount": 0, "color": getHexColor(prob)}

    elif name == "Eleiçöes":
        return {"name": name, "type": "eleicoes", "amount": 0, "color": getHexColor(prob)}

    elif name == "Fraude":
        return {"name": name, "type": "fraude", "amount": 0, "color": getHexColor(prob)}

    elif name == "Feminicídio":
        return {"name": name, "type": "contra_a_vida", "amount": 0, "color": getHexColor(prob)}

    elif name == "Furto":
        return {"name": name, "type": "furto", "amount": 0, "color": getHexColor(prob)}

    elif name == "Homicídio":
        return {"name": name, "type": "contra_a_vida", "amount": 0, "color": getHexColor(prob)}

    elif name == "Incêndio":
        return {"name": name, "type": "incendio", "amount": 0, "color": getHexColor(prob)}

    elif name == "Inválido":
        return {"name": name, "type": "invalido", "amount": 0, "color": getHexColor(prob)}

    elif name == "Latrocínio":
        return {"name": name, "type": "contra_a_vida", "amount": 0, "color": getHexColor(prob)}

    elif name == "Lesão corporal":
        return {"name": name, "type": "contra_a_pessoa", "amount": 0, "color": getHexColor(prob)}

    elif name == "Meio ambiente":
        return {"name": name, "type": "meio_ambiente", "amount": 0, "color": getHexColor(prob)}

    elif name == "Operação policial militar":
        return {"name": name, "type": "operacao_policial_militar", "amount": 0, "color": getHexColor(prob)}

    elif name == "Outras infrações penais":
        return {"name": name, "type": "outras_infracoes_penais", "amount": 0, "color": getHexColor(prob)}

    elif name == "Outros acidentes":
        return {"name": name, "type": "outros_acidentes", "amount": 0, "color": getHexColor(prob)}

    elif name == "Pertubação do trabalho":
        return {"name": name, "type": "pertubacao_do_trabalho", "amount": 0, "color": getHexColor(prob)}

    elif name == "Perturbação do trabalho ou sossego alheios":
        return {"name": name, "type": "pertubacao_do_trabalho", "amount": 0, "color": getHexColor(prob)}

    elif name == "Roubo":
        return {"name": name, "type": "roubo", "amount": 0, "color": getHexColor(prob)}

    elif name == "Roubo a pedestre":
        return {"name": name, "type": "roubo", "amount": 0, "color": getHexColor(prob)}

    elif name == "Roubo de veículo":
        return {"name": name, "type": "roubo", "amount": 0, "color": getHexColor(prob)}

    elif name == "Samu":
        return {"name": name, "type": "samu", "amount": 0, "color": getHexColor(prob)}

    elif name == "Saúde":
        return {"name": name, "type": "saude", "amount": 0, "color": getHexColor(prob)}

    elif name == "Sistema prisional":
        return {"name": name, "type": "sistema_prisional", "amount": 0, "color": getHexColor(prob)}

    elif name == "Traffic":
        return {"name": name, "type": "conflito_transito", "amount": prob, "color": getHexColor(prob)}

    elif name == "Crime":
        return {"name": name, "type": "roubo", "amount": prob, "color": getHexColor(prob)}

    elif name == "By Law":
        return {"name": name, "type": "contra_a_pessoa", "amount": prob, "color": getHexColor(prob)}

    elif name == "Miscellaneous":
        return {"name": name, "type": "contra_a_vida", "amount": prob, "color": getHexColor(prob)}

    else:
        return {"name": name, "type": "invalido", "amount": 0, "color": getHexColor(prob)}


def getHexColor(prob):
    if prob >= 60:
        return '#F93C1A'
    elif prob >= 30:
        return '#FFD859'
    elif prob >= 0:
        return '#098765'
    else:
        return '#D3D3D3'


