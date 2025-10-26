from xml.etree import ElementTree as ET

input_file = "opriri.kml"
max_points_per_link = 25

# Namespace KML
ns = {"kml": "http://www.opengis.net/kml/2.2"}

# Citește fișierul XML
tree = ET.parse(input_file)
root = tree.getroot()

# Extrage coordonatele din toate <Point> în ordinea apariției
coords_list = []
for placemark in root.findall(".//kml:Placemark", ns):
    point = placemark.find(".//kml:Point", ns)
    if point is not None:
        coords = point.find("kml:coordinates", ns).text.strip()
        lon, lat = map(float, coords.split(",")[:2])
        coords_list.append(f"{lat},{lon}")

# Împarte coordonatele în porțiuni consecutive
def split_into_chunks(lst, size):
    for i in range(0, len(lst), size):
        yield lst[i:i + size]

# Generează linkuri Google Maps
base_url = "https://www.google.com/maps/dir/"
print("🔗 Linkuri Google Maps pe porțiuni consecutive:\n")

for i, chunk in enumerate(split_into_chunks(coords_list, max_points_per_link)):
    route_url = base_url + "/".join(chunk)
    print(f"Link {i+1} (Puncte {i*max_points_per_link+1}–{i*max_points_per_link+len(chunk)}):")
    print(route_url + "\n")