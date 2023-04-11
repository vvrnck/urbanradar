import psycopg2
import os
from sqlalchemy import create_engine, text
import ast
import json


def get_connection(database_URI):
    # Connect to the Postgres database
    engine = create_engine(database_URI)
    return engine


def extract_data():
    # Extract data from the csv file and import into the Postgres database
    # The csv file is located in the event-file folder
    # The csv file is named events.csv
    # The csv file has the following columns:
    # date, lat, lng
    # The csv file has the following format:
    # 2018-01-01, -23.123456, -46.123456
    database_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    engine = get_connection(database_URI)
    with engine.connect() as conn:
        with open('event-file/events.csv', 'r') as f:
            # Loop through row to find the date and lat and lng in the header
            row = f.readline().split(',')
            for ind, r in enumerate(row):
                if r == 'date':
                    date_ind = ind
                if r == 'lat':
                    lat_ind = ind
                if r == 'lng':
                    lng_ind = ind

            # Use schema datalake
            conn.execute(text("SET search_path TO web"))

            results = conn.execute(text('Select * from "Feature"')).fetchall()
            coordinates = ast.literal_eval(results[0][5])
            print(len(coordinates))
            cleaned_coordinates = '(('
            for i, row in enumerate(coordinates):
                # Get the geometry column
                coords = row
                lat, long = coords[0], coords[1]
                cleaned_coordinates += f"{lat} {long}"
                if i != len(coordinates)-1:
                    cleaned_coordinates += ", "
                else:
                    cleaned_coordinates += "))"
            print(cleaned_coordinates)

            print('Data imported successfully!')


def open_geojson_and_create_feature():
    database_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    engine = get_connection(database_URI)
    with engine.connect() as conn:
        with open('grid.geojson', 'r') as f:
            data = json.load(f)
        conn.execute(text("SET search_path TO web"))
        for feature in data['features']:
            # assuming each feature has only one geometry object
            coordinates = feature['geometry']['coordinates']
            cleaned_coordinates = '(('
            list_coordinates = []
            for i, row in enumerate(coordinates[0]):
                # Get the geometry column
                coords = row
                lat, long = coords[1], coords[0]
                cleaned_coordinates += f"{lat} {long}"
                list_coordinates.append([lat, long])
                if i != len(coordinates[0])-1:
                    cleaned_coordinates += ", "
            cleaned_coordinates += "))"
            coordinates = str(list_coordinates)
            print(cleaned_coordinates)
            print(coordinates)
            conn.execute(text(
                'INSERT INTO "Feature" (code, tenant_id, layer_id, feature_collection_id, geometry, type, view) VALUES (1, 1, 1, 1, \'{}\', \'POLYGON\', \'{}\')'.format(str(list_coordinates), str(cleaned_coordinates))))
        conn.commit()


def run():
    open_geojson_and_create_feature()


if __name__ == '__main__':
    run()
