from shapely.geometry import Point
import pandas as pd
import geopandas as gpd
from geopandas.tools import sjoin


def find_file_extension(name):
    try:
        return name.split('.')[-1]
    except IndexError:
        return ''


def from_csv_to_geojson(target_file, col_lat, col_long):
    target_df = pd.read_csv(target_file)

    data = {'DATAHORA': [], 'lat': [], 'lng': [], 'coordinates': []}

    for index, pol in target_df.iterrows():
        if pol[col_lat] != "IRT" and pol[col_long] != "IRT" and pol[col_lat] != "0" and pol[col_long] != "0":
            pol[col_lat] = float(pol[col_lat])
            pol[col_long] = float(pol[col_long])

            data['lat'].append(pol[col_lat])
            data['lng'].append(pol[col_long])
            data['DATAHORA'].append(pol['DATAHORA'])

    data['coordinates'] = list(zip(data['lat'], data['lng']))
    target = pd.DataFrame(
        data, columns=['DATAHORA', 'lat', 'lng', 'coordinates'])
    # print(target)
    target['coordinates'] = target['coordinates'].apply(Point)
    return gpd.GeoDataFrame(
        target,
        geometry='coordinates',
        crs='+init=epsg:4326'
    )


def get_centroid():
    target_df = gpd.read_file('city-hex-polygons-9.geojson')
    for i in range(len(target_df)):
        target_df['geometry'][i] = target_df['geometry'][i].centroid

    target_df.to_file("city-hex-polygons-9-centroid.geojson", driver='GeoJSON')


def run(target_file, polygonos_file, col_lat, col_long, output_name_file):
    extension_target_file = find_file_extension(target_file)
    if extension_target_file == 'csv':
        print('\t\t- CONVERTENDO ARQUIVO DE EVENTOS PARA O FORMATO GEOJSON')
        target_gdf = from_csv_to_geojson(target_file, col_lat, col_long)
    elif extension_target_file == 'geojson':
        print("\t\t- LENDO ARQUIVO DE EVENTOS")
        target_gdf = gpd.read_file(target_file)
    else:
        raise Exception(
            '### Error: target file format must be csv or geojson.')

    print('\t\t- LENDO ARQUIVO DE POLIGONOS')
    polygonos_gdf = gpd.read_file(polygonos_file)
    print('\t\t- REALIZANDO JUNCAO ENTRE AS LOCALIZACOES')
    try:
        teste_df = sjoin(target_gdf, polygonos_gdf, how="left")
    except AttributeError as err:
        print("\t\t - Ocorreu um, verifique se spatialindex está instalada.")
        print("\t\t\t", err)
        return False

    print(f'\t\t- GERANDO AQRUIVO {output_name_file}')
    if extension_target_file.lower() == 'geojson':
        teste_df.to_file(output_name_file, driver='GeoJSON')
        return True
    elif extension_target_file.lower() == 'csv':
        df_out = pd.DataFrame(teste_df).dropna()
        print(df_out)
        if not df_out.empty:
            if "id" in df_out.keys():
                resp = df_out['id'].str.split('_', expand=True)
                if len(resp.columns) == 2:
                    df_out[['x_index', 'y_index']] = resp
            df_out["DATAHORA"] = df_out["DATAHORA"].astype("string")
            df_out.to_csv(output_name_file, index=None, header=True)
            return True
        else:
            return False


if __name__ == '__main__':
    run('./event-file/events.csv',
        'output.geojson', 'lat', 'lng', 'output2.geojson')
