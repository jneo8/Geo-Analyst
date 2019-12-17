"""Main."""
import csv
import time
import functools
import json
import pandas as pd
from neologger import logger

# Folium
from folium import Map, GeoJson, Marker
from folium.plugins import MarkerCluster


logger = logger.Logger(__name__)


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
        location=[25.105497, 121.597366],  # Taipei's latitude longitude.,
        zoom_start=11,
        tiles="cartodbpositron",
        attr="""© <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors © <a href="http://cartodb.com/attributions#basemaps">CartoDB</a>""",
    )

    mc = MarkerCluster()

    for index, row in df.iterrows():
        logger.debug(f"{index}: {row}")
        geo_json = json.loads(row["geoJSON"])
        logger.debug(geo_json)
        for feature in geo_json["features"]:
            point = feature["geometry"]["coordinates"]
            mk = Marker(location=point)
            mk.add_to(mc)
    mc.add_to(m)
    m.save("./source/quickVisualizationOnMap.html")


@timeit
def main():
    """Main."""
    df = read_data()
    logger.info(df.head())
    quickVisualizationOnMap(df)


if __name__ == "__main__":
    main()
