"""Main."""
import csv
import time
import sys
import functools
import json
import pandas as pd
from neologger import logger

# Folium
import folium
from folium import Map, GeoJson, Marker
from folium.plugins import MarkerCluster

# H3
from h3 import h3

# Geojson
from geojson.feature import Feature, FeatureCollection

# ColorMap
import branca.colormap as cm


logger = logger.Logger(__name__)

csv.field_size_limit(sys.maxsize)

TAIPEI_LOCATION = [25.105497, 121.597366]

COLORS = {
	"indigo":"#4B0082",
	"gold":"#FFD700",
	"hotpink":"#FF69B4",
	"firebrick":"#B22222",
	"indianred":"#CD5C5C",
	"sage":"#87AE73",
	"yellow":"#FFFF00",
	"mistyrose":"#FFE4E1",
	"darkolivegreen":"#556B2F",
	"olive":"#808000",
	"darkseagreen":"#8FBC8F",
	"pink":"#FFC0CB",
	"tomato":"#FF6347",
	"lightcoral":"#F08080",
	"orangered":"#FF4500",
	"navajowhite":"#FFDEAD",
	"lime":"#00FF00",
	"palegreen":"#98FB98",
	"greenyellow":"#ADFF2F",
	"burlywood":"#DEB887",
	"seashell":"#FFF5EE",
	"mediumspringgreen":"#00FA9A",
	"fuchsia":"#FF00FF",
	"papayawhip":"#FFEFD5",
	"blanchedalmond":"#FFEBCD",
	"chartreuse":"#7FFF00",
	"dimgray":"#696969",
	"black":"#000000",
	"peachpuff":"#FFDAB9",
	"springgreen":"#00FF7F",
	"aquamarine":"#7FFFD4",
	"white":"#FFFFFF",
	"b":"#0000FF",
	"orange":"#FFA500",
	"lightsalmon":"#FFA07A",
	"darkslategray":"#2F4F4F",
	"brown":"#A52A2A",
	"ivory":"#FFFFF0",
	"dodgerblue":"#1E90FF",
	"peru":"#CD853F",
	"lawngreen":"#7CFC00",
	"chocolate":"#D2691E",
	"crimson":"#DC143C",
	"forestgreen":"#228B22",
	"slateblue":"#6A5ACD",
	"lightseagreen":"#20B2AA",
	"cyan":"#00FFFF",
	"mintcream":"#F5FFFA",
	"silver":"#C0C0C0",
	"antiquewhite":"#FAEBD7",
	"mediumorchid":"#BA55D3",
	"skyblue":"#87CEEB",
	"gray":"#808080",
	"darkturquoise":"#00CED1",
	"goldenrod":"#DAA520",
	"darkgreen":"#006400",
	"floralwhite":"#FFFAF0",
	"darkviolet":"#9400D3",
	"darkgray":"#A9A9A9",
	"moccasin":"#FFE4B5",
	"saddlebrown":"#8B4513",
	"darkslateblue":"#483D8B",
	"lightskyblue":"#87CEFA",
	"lightpink":"#FFB6C1",
	"mediumvioletred":"#C71585",
	"r":"#FF0000",
	"red":"#FF0000",
	"deeppink":"#FF1493",
	"limegreen":"#32CD32",
	"k":"#000000",
	"darkmagenta":"#8B008B",
	"palegoldenrod":"#EEE8AA",
	"plum":"#DDA0DD",
	"turquoise":"#40E0D0",
	"m":"#FF00FF",
	"lightgoldenrodyellow":"#FAFAD2",
	"darkgoldenrod":"#B8860B",
	"lavender":"#E6E6FA",
	"maroon":"#800000",
	"yellowgreen":"#9ACD32",
	"sandybrown":"#FAA460",
	"thistle":"#D8BFD8",
	"violet":"#EE82EE",
	"navy":"#000080",
	"magenta":"#FF00FF",
	"tan":"#D2B48C",
	"rosybrown":"#BC8F8F",
	"olivedrab":"#6B8E23",
	"blue":"#0000FF",
	"lightblue":"#ADD8E6",
	"ghostwhite":"#F8F8FF",
	"honeydew":"#F0FFF0",
	"cornflowerblue":"#6495ED",
	"linen":"#FAF0E6",
	"darkblue":"#00008B",
	"powderblue":"#B0E0E6",
	"seagreen":"#2E8B57",
	"darkkhaki":"#BDB76B",
	"snow":"#FFFAFA",
	"sienna":"#A0522D",
	"mediumblue":"#0000CD",
	"royalblue":"#4169E1",
	"lightcyan":"#E0FFFF",
	"green":"#008000",
	"mediumpurple":"#9370DB",
	"midnightblue":"#191970",
	"cornsilk":"#FFF8DC",
	"paleturquoise":"#AFEEEE",
	"bisque":"#FFE4C4",
	"slategray":"#708090",
	"darkcyan":"#008B8B",
	"khaki":"#F0E68C",
	"wheat":"#F5DEB3",
	"teal":"#008080",
	"darkorchid":"#9932CC",
	"deepskyblue":"#00BFFF",
	"salmon":"#FA8072",
	"y":"#FFFF00",
	"darkred":"#8B0000",
	"steelblue":"#4682B4",
	"g":"#008000",
	"palevioletred":"#DB7093",
	"lightslategray":"#778899",
	"aliceblue":"#F0F8FF",
	"lightgreen":"#90EE90",
	"orchid":"#DA70D6",
	"gainsboro":"#DCDCDC",
	"mediumseagreen":"#3CB371",
	"lightgray":"#D3D3D3",
	"c":"#00FFFF",
	"mediumturquoise":"#48D1CC",
	"darksage":"#598556",
	"lemonchiffon":"#FFFACD",
	"cadetblue":"#5F9EA0",
	"lightyellow":"#FFFFE0",
	"lavenderblush":"#FFF0F5",
	"coral":"#FF7F50",
	"purple":"#800080",
	"aqua":"#00FFFF",
	"lightsage":"#BCECAC",
	"whitesmoke":"#F5F5F5",
	"mediumslateblue":"#7B68EE",
	"darkorange":"#FF8C00",
	"mediumaquamarine":"#66CDAA",
	"darksalmon":"#E9967A",
	"beige":"#F5F5DC",
	"w":"#FFFFFF",
	"blueviolet":"#8A2BE2",
	"azure":"#F0FFFF",
	"lightsteelblue":"#B0C4DE",
	"oldlace":"#FDF5E6"
}


def timeit(func):
    """Log function execute duration."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_timestamp = time.time()
        result = func(*args, **kwargs)
        logger.info(
            'time cost {duration}'.format(
                duration=time.time() - start_timestamp
            )
        )
        return result

    return wrapper

def read_data():
    """Read data from csv and return pandas dataFrame."""
    with open("./src/classifier_output.csv") as csv_file:
        rows = csv.reader(csv_file)
        headers = next(rows, None)
        arr = []
        for row in rows:
            arr.append(row)
        df = pd.DataFrame(arr, columns = headers)
        return df

def quickVisualizationOnMap(df=pd.DataFrame()):
    m = Map(
        location=TAIPEI_LOCATION,  # Taipei's latitude longitude.,
        zoom_start=11,
        tiles="cartodbpositron",
        attr="""© <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors © <a href="http://cartodb.com/attributions#basemaps">CartoDB</a>""",
    )

    mc = MarkerCluster()

    for index, row in df.iterrows():
        geo_json = json.loads(row["geoJSON"])
        for feature in geo_json["features"]:
            point = feature["geometry"]["coordinates"]
            mk = Marker(location=point)
            mk.add_to(mc)
    mc.add_to(m)
    m.save("./source/quickVisualizationOnMap.html")


def counts_by_hexagon(df):
    """Use h3.geo_to_h3 to index each data point into the spatial index of the specified resolution.
              Use h3.h3_to_geo_boundary to obtain the geometries of these hexagons"""

    data = {}
    for index, row in df.iterrows():
        k = int(row["group"])


        data[k] = {
            "h3_idxs": set(row["H3Indexs"].split(",")),
        }

    df_arr = []
    for k, v in data.items():
        for h3_idx in v["h3_idxs"]:
            geometry = {"type": "Polygon", "coordinates": [h3.h3_to_geo_boundary(h3_address=h3_idx, geo_json=True)]}
            df_arr.append([h3_idx, k, geometry])
    df = pd.DataFrame(df_arr, columns=["hex_id", "value", "geometry"])
    return df

def hexagons_dataframe_to_geojson(df_hex, file_output = None):
    '''Produce the GeoJSON for a dataframe that has a geometry column in geojson format already, along with the columns hex_id and value '''
    list_features = []
    for i,row in df_hex.iterrows():
        feature = Feature(
            geometry = row["geometry"],
            id=row["hex_id"],
            properties = {"value" : row["value"]}
        )
        list_features.append(feature)
    feat_collection = FeatureCollection(list_features)
    geojson_result = json.dumps(feat_collection)
    #optionally write to file
    if file_output is not None:
        with open(file_output,"w") as f:
            json.dump(feat_collection,f)
    return geojson_result


def choropleth_map(
    df,
    border_color="black",
    fill_opacity=0.7,
    initial_map=None,
    with_legend=False,
    kind="linear",
    layer_prefix="",
    colors=list(COLORS.keys())[:9],
):

    # colormap
    min_value = df["value"].min()
    max_value = df["value"].max()
    m = round ((min_value + max_value ) / 2 , 0)

    # Get resolution from first idx.
    res = h3.h3_get_resolution(df.loc[0,'hex_id'])

    if initial_map is None:
        initial_map = Map(
            location=TAIPEI_LOCATION,
            zoom_start=11,
            tiles="Stamen Terrain",
            attr= '© <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors © <a href="http://cartodb.com/attributions#basemaps">CartoDB</a>',
        )

    # Color map
    # color names accepted https://github.com/python-visualization/branca/blob/master/branca/_cnames.json
    if kind == "linear":
        custom_cm = cm.LinearColormap(colors, vmin=min_value, vmax=max_value)
    elif kind == "outlier":
        custom_cm = cm.LinearColormap(["blue", "white", "red"], vmin=min_value, vmax=max_value)
    elif kind == "filled_nulls":
        custom_cm = cm.LinearColormap(["sienna", "green", "yollow", "red"], index=[0, min_value, max_value], vmin=min_value, vmax=max_value)


    geo_json = hexagons_dataframe_to_geojson(df_hex=df)

    # plot on map
    name_layer = f"Choropleth_{res}_{kind}_{layer_prefix}"

    GeoJson(
        geo_json,
        style_function=lambda feature: {
            "fillColor": custom_cm(0),
            "color": border_color,
            "weight": 1,
            "fillOpacity": fill_opacity,
            "popup": "123",
        },
        name=name_layer,
    ).add_to(initial_map)

    if with_legend == True:
        custom_cm.add_to(initial_map)
    return initial_map

@timeit
def main():
    """Main."""
    df = read_data()
    logger.info(df.head())
    quickVisualizationOnMap(df)

    m_hex_map = None
    for row in df.itertuples():
        dff = pd.DataFrame(data=[row], columns=["index"] + df.columns.tolist())
        color_num = int(row.group) * 8
        colors = list(COLORS.keys())[color_num:color_num+2]
        m_hex_map = choropleth_map(
            df=counts_by_hexagon(dff),
            with_legend=False,
            initial_map=m_hex_map,
            layer_prefix=row.group,
            colors=colors,
        )
    folium.map.LayerControl('bottomright', collapsed=False).add_to(m_hex_map)
    m_hex_map.save("./source/m_hex.html")


if __name__ == "__main__":
    main()
