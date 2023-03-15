import datetime
import json
from h3 import h3
import click

# Receber um lat long e processar com o h3 do uber
# https://github.com/uber/h3

# Converter o h3 para um geojson
def create_first_user():
    pass

def create_coord(latlng):
    geoJson = {
        "coordinates":  [latlng],
        "type": "Polygon"
    }
    hexagons = h3.polyfill(geoJson, 8)

    print(h3.h3_to_geo_boundary(list(hexagons)[0], geo_json=True))


    geojson_out = {
    "type": "FeatureCollection",
    "features": []
    }

    for i in hexagons:
        geojson_out["features"].append({
        "type": "Feature",
        "properties": {
            "identifier": i
        },
        "geometry": {
            "type": "Polygon",
            "coordinates": [
                [(coord[1], coord[0]) for coord in h3.h3_to_geo_boundary(i, geo_json=True)]
            ]
        }
        })
            

    with open("output.geojson", "w") as outfile:
        json.dump(geojson_out, outfile)

@click.command()
@click.option('--latlng','-l',multiple=True, required=False, help='Lat and Lng in a list like: [[30.04624344244843,5.869425069651257],[29.888186738810248,5.809930193157186],[30.069843858445182,5.692640298902774],[30.203693679544443,5.754981028231114],[30.04624344244843,5.869425069651257]]')
def run(latlng):
    click.echo(latlng)
    create_coord(latlng)


if __name__ == '__main__':
    run()