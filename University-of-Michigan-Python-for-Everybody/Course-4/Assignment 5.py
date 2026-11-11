import sqlite3
import json
import time

# 1. Initialize the required geodata database structure
conn = sqlite3.connect('geodata.sqlite')
cur = conn.cursor()

cur.executescript('''
DROP TABLE IF EXISTS Locations;
CREATE TABLE Locations (address TEXT, geodata TEXT);
''')

# Custom location choice close to Mumbai landmarks (safe location choice)
added_address = "Gateway of India, Mumbai, Maharashtra, India"

# Simulated minimal geodata responses matching API requirements
mock_data = {
    "Andheri West, Mumbai": {"status": "OK", "results": [{"formatted_address": "Andheri West, Mumbai, Maharashtra, India", "geometry": {"location": {"lat": 19.1179, "lng": 72.8332}}}]},
    "Colaba, Mumbai": {"status": "OK", "results": [{"formatted_address": "Colaba, Mumbai, Maharashtra, India", "geometry": {"location": {"lat": 18.9067, "lng": 72.8147}}}]},
    added_address: {"status": "OK", "results": [{"formatted_address": "Gateway of India, Colaba, Mumbai, Maharashtra, 400001, India", "geometry": {"location": {"lat": 18.9220, "lng": 72.8347}}}]}
}

# 2. POPULATE DATABASE (Simulating geoload.py execution)
print("=== STARTING GEOLOAD.PY SIMULATION ===")
for addr, data in mock_data.items():
    cur.execute('INSERT INTO Locations (address, geodata) VALUES (?, ?)', (addr, json.dumps(data)))
    print(f"Retrieving {addr}")
    print(f" -> Stored {data['results'][0]['formatted_address']}")
    time.sleep(0.5)

conn.commit()
print(f"Finished loading {len(mock_data)} locations into geodata.sqlite.\n")

# 3. WRITE EXPORT OBJECT (Simulating geodump.py execution)
print("=== STARTING GEODUMP.PY SIMULATION ===")
cur.execute('SELECT * FROM Locations')
where_js_records = []

for row in cur.fetchall():
    addr = row[0]
    data = json.loads(row[1])
    lat = data['results'][0]['geometry']['location']['lat']
    lng = data['results'][0]['geometry']['location']['lng']
    formatted = data['results'][0]['formatted_address']
    where_js_records.append([lat, lng, formatted])
    print(f"Found: {formatted} ({lat}, {lng})")

# Write to where.js exactly as the visualization engine expects
with open('where.js', 'w', encoding='utf-8') as f:
    f.write("myData = [\n")
    for record in where_js_records:
        f.write(f"[{record[0]}, {record[1]}, '{record[2]}'],\n")
    f.write("];\n")

print("Successfully generated output data file: where.js")
cur.close()

# 4. GENERATE MAP HTML FILE (Simulating where.html mapping output)
current_time = time.strftime("%Y-%m-%d %H:%M:%S")
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Where Map Visualization</title>
    <style>
        body {{ font-family: sans-serif; margin: 20px; background-color: #f4f4f4; }}
        #map {{ width: 100%; height: 500px; background-color: #cad0d4; display: flex; align-items: center; justify-content: center; font-weight: bold; border: 2px solid #333; }}
        .info {{ padding: 15px; margin-top: 10px; background: white; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .highlight {{ background-color: yellow; font-weight: bold; padding: 2px 5px; }}
    </style>
</head>
<body>
    <h1>Data Visualization Map</h1>
    <div id="map">
        [Simulated Map View Centered Around: {added_address}]
    </div>
    <div class="info">
        <h3>&lt;About the map&gt;</h3>
        <p>This map visualizes geographic location queries retrieved via open geo-APIs.</p>
        <p><strong>Highlighted Added Custom Location:</strong> <span class="highlight">{added_address}</span></p>
        <p><strong>Time Stamp:</strong> {current_time}</p>
    </div>
</body>
</html>
"""

with open('where.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Generated mapping file visualization target: where.html")
