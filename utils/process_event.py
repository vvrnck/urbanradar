import psycopg2
import os
from sqlalchemy import create_engine, text


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
                print(r)
                if 'date' in r:
                    date_ind = ind
                if r == 'lat':
                    lat_ind = ind
                if r == 'lng':
                    lng_ind = ind

            # Use schema datalake
            conn.execute(text("SET search_path TO datalake"))
            for row in f:
                row_splited = row.split(',')
                print(row_splited[date_ind])
                conn.execute(text(
                    "INSERT INTO events (date, lat, lng) VALUES ('{0}',{1},{2})".format(row_splited[date_ind], row_splited[lat_ind], row_splited[lng_ind])))
                print("INSERT INTO events (date, lat, lng) VALUES ({0},{1},{2})".format(
                    row_splited[date_ind], row_splited[lat_ind], row_splited[lng_ind]))
                conn.commit()
            print('Data imported successfully!')


def run():
    extract_data()


if __name__ == '__main__':
    run()
