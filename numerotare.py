import simplekml
from xml.etree import ElementTree as ET

input_file = "opriri.kml"
output_file = "opriri_numerotate.kml"

# Namespace KML
ns = {"kml": "http://www.opengis.net/kml/2.2"}

# Citește fișierul XML
tree = ET.parse(input_file)
root = tree.getroot()

# Extrage punctele de oprire
stop_points = []
for placemark in root.findall(".//kml:Placemark", ns):
    point = placemark.find(".//kml:Point", ns)
    if point is not None:
        coords = point.find("kml:coordinates", ns).text.strip()
        lon, lat = map(float, coords.split(",")[:2])
        stop_points.append((lat, lon))

# Creează fișierul KML nou cu puncte numerotate
kml = simplekml.Kml()
for i, (lat, lon) in enumerate(stop_points, start=1):
    p = kml.newpoint(name=f"Oprire {i}", coords=[(lon, lat)])
    p.style.iconstyle.color = simplekml.Color.red

# Salvează fișierul
kml.save(output_file)
print(f"Fișierul cu opriri numerotate a fost salvat ca: {output_file}")