import json
import sys
from app import create_app, db
from app.model import Tenant, Layer, FeatureCollection, Feature

def geojson_to_wkt(geom, type_geom):
    geo_i = []
    for lat_lng in geom[0]:
        lat = float(lat_lng[0])
        lng = float(lat_lng[1])
        geo_i.append("{0} {1}".format(lng, lat))

    geo_out = "{0}(({1}))".format(type_geom.upper(), ",".join(geo_i))
    return geo_out

def insert_feature_mesh(input_file, layer_id, tenant_id, feature_collection_id, external_id_col_key):    
    # read and parse JSON file
    with open(input_file, 'r') as myfile:
        data = myfile.read()
    obj = json.loads(data)

   
    for feature in obj['features']:
        #external_id = "{0} {1}".format(col_key, feature["properties"][external_id_col_key])
        
        geo_out = ""
        if feature["geometry"]["type"] == "GeometryCollection":
            geom_collection = []
            for geom in feature["geometry"]["geometries"]:
                wkt = geojson_to_wkt(geom["coordinates"], geom["type"])
                geom_collection.append(wkt)
            geo_out = "GEOMETRYCOLLECTION({0})".format(",".join(geom_collection))
        else:
            polygon = feature["geometry"]["coordinates"]
            geo_out = geojson_to_wkt(polygon, feature["geometry"]["type"])

        geo_txt_out = json.dumps(feature["geometry"])

        # create Feature instance
        new_feature = Feature(
            tenant_id=int(tenant_id),
            layer_id=int(layer_id),
            code="external_id",
            geometry=geo_out,
            feature_collection_id=int(feature_collection_id),
            type=feature["geometry"]["type"]
        )

        db.session.add(new_feature)
    
    db.session.commit()

if __name__ == "__main__":
    try:
        path_geojson = sys.argv[1]
    except IndexError:
        print("### Error: geojson file path not found")
        exit()

    try:
        id_layer = sys.argv[2]
    except IndexError:
        print("### Error: id_layer not found")
        exit()

    try:
        tenant_id = sys.argv[3]
    except IndexError:
        print("### Error: tenant_id not found")
        exit()

    try:
        feature_collection_id = sys.argv[4]
    except IndexError:
        print("### Error: feature_collection_id not found")
        exit()

    try:
        external_id_col_key = sys.argv[5]
    except IndexError:
        print("### Error: column external_id not found")
        exit()

     # create the application instance
    app = create_app()
    with app.app_context():
        insert_feature_mesh(path_geojson, id_layer, tenant_id, feature_collection_id, external_id_col_key)
