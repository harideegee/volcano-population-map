import folium
import pandas

data = pandas.read_csv("volcanoes.txt")
lat = list(data["Latitude"])
lon = list(data["Longitude"])
name = list(data["Volcano Name"])
elev = list(data["Elev"])
reg = list(data["Region"])

html = """<h4>Volcano information:</h4>
Name: %s <br>
Elevation: %s m <br>
Region: %s <br>
"""

def icon_color(elevation):
    if elevation < 1000:
        return "green"
    elif 1000 <= elevation <= 3000:
        return "orange"
    else:
        return "red"

map = folium.Map(location=[38.58, -99.09], zoom_start=6, tiles="Stamen Terrain")

markers = folium.FeatureGroup(name="Volcano Markers")

for lt, ln, nm, el, rg in zip(lat, lon, name, elev, reg):
    iframe = folium.IFrame(html=html %(nm, str(el), rg), width=200, height=100)
    markers.add_child(folium.CircleMarker(location=[lt, ln], radius=6, popup=folium.Popup(iframe), fill_color=icon_color(el), color="grey", fill_opacity=0.7))

polygons = folium.FeatureGroup(name="Population Layer")

polygons.add_child(folium.GeoJson(data=open("world.json", "r", encoding="utf-8-sig").read(), style_function=lambda x: {"fillColor": "green" if x["properties"]["POP2005"] < 10000000 else "orange" if 10000000 <= x["properties"]["POP2005"] < 20000000 else "red"}))


map.add_child(markers)
map.add_child(polygons)
map.add_child(folium.LayerControl())

map.save("Map1.html")