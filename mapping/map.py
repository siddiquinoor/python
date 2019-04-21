import folium
import pandas

data = pandas.read_csv("Volcanoes_USA.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])


def color_selector(elevation):
    if elevation < 1000:
        return 'green'
    elif 1000 <= elevation < 3000:
        return 'orange'
    else:
        return 'red'


maps = folium.Map(location=[42.605899799999996, -117.5810013], zoom_start=6, tiles="Mapbox Bright")

fg = folium.FeatureGroup(name="My Map")

for lt, ln, el in zip(lat, lon, elev):
    fg.add_child(folium.CircleMarker(location=[lt, ln], radius=6, popup=str(el)+" m" + " Lat: " + str(lt) + " Lon: " + str(ln), fill_color=color_selector(el), color="gray", fill_opacity="0.7"))

maps.add_child(fg)

maps.save("Map1.html")
