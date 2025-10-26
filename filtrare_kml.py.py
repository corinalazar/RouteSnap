import simplekml
from geopy.distance import geodesic
from xml.etree import ElementTree as ET

input_file = "traseu.kml"
output_file = "opriri.kml"

# Citește fișierul XML
tree = ET.parse(input_file)
root = tree.getroot()

# Namespace KML
ns = {"kml": "http://www.opengis.net/kml/2.2"}

# Extrage punctele de oprire (doar cele cu <b>Stop</b> în descriere)
stop_points = []
for placemark in root.findall(".//kml:Placemark", ns):
    point = placemark.find(".//kml:Point", ns)
    desc = placemark.find("kml:description", ns)
    if point is not None and desc is not None and "<b>Stop</b>" in desc.text:
        coords = point.find("kml:coordinates", ns).text.strip()
        lon, lat = map(float, coords.split(",")[:2])
        name = placemark.find("kml:name", ns)
        stop_points.append((lat, lon, name.text if name is not None else " "))

# Creează fișierul KML nou
kml = simplekml.Kml()

# Adaugă punctele de oprire (roșu)
for i, (lat, lon, name) in enumerate(stop_points):
    p = kml.newpoint(name=name, coords=[(lon, lat)])
    p.style.iconstyle.color = simplekml.Color.red



# Salvează fișierul
kml.save(output_file)
print(f"Fișierul combinat a fost salvat ca: {output_file}")