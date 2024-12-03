import re
from math import radians, sin, cos, sqrt, atan2

# Fonction pour convertir les coordonnées NMEA (ddmm.mmmm) en degrés décimaux
def nmea_to_decimal(coord, direction):
    degrees = int(coord[:2])
    minutes = float(coord[2:])
    decimal = degrees + (minutes / 60)
    if direction in ['S', 'W']:
        decimal *= -1
    return decimal

# Fonction pour calculer la distance entre deux points GPS (Haversine)
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Rayon de la Terre en km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

# Lecture du fichier NMEA
positions = []
with open("trames.nmea", "r") as file:
    for line in file:
        if line.startswith("$GPRMC"):
            fields = line.split(",")
            if fields[2] == "A":  # Statut actif
                lat = nmea_to_decimal(fields[3], fields[4])
                lon = nmea_to_decimal(fields[5], fields[6])
                speed = float(fields[7]) * 1.852  # Convertir nœuds en km/h
                positions.append((lat, lon, speed))

# Calcul des distances et vitesse moyenne
total_distance = 0
for i in range(1, len(positions)):
    total_distance += haversine(positions[i - 1][0], positions[i - 1][1], positions[i][0], positions[i][1])

average_speed = sum(p[2] for p in positions) / len(positions)

# Génération de la page HTML avec carte Leaflet
html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Résultats NMEA GPS</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
	<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
        }}
        h1 {{
            color: #333;
        }}
        #map {{
            height: 500px;
            margin: 20px auto;
            width: 80%;
        }}
    </style>
</head>
<body>
    <h1>Analyse des trames NMEA GPS</h1>
    <p><strong>Distance totale parcourue :</strong> {total_distance:.2f} km</p>
    <p><strong>Vitesse moyenne :</strong> {average_speed:.2f} km/h</p>
    <h2>Carte des positions GPS</h2>
    <div id="map"></div>
    <script>
        // Initialisation de la carte
        var map = L.map('map').setView([{positions[0][0]}, {positions[0][1]}], 13);

        // Ajouter une couche OpenStreetMap()
        L.tileLayer('https://s.tile.openstreetmap.org/z/x/y.png',
        {{
            maxZoom: 19,
            attribution: '© OpenStreetMap'
        }}).addTo(map);

        // Ajouter les positions GPS comme marqueurs sur la carte
        var positions = {positions};
        positions.forEach(function(pos) {{
            L.marker([pos[0], pos[1]]).addTo(map)
                .bindPopup('Vitesse: ' + pos[2].toFixed(2) + ' km/h');
        }});
    </script>
</body>
</html>
"""

# Sauvegarde du fichier HTML
output_file = "resultats_carte.html"
with open(output_file, "w") as file:
    file.write(html_content)

print(f"Les résultats ont été enregistrés dans le fichier {output_file}.")
