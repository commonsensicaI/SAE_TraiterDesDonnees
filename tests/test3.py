import re
from math import radians, sin, cos, sqrt, atan2
import folium

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
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
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

# Génération de la carte avec Folium
if positions:
    # Point de départ pour centrer la carte
    start_location = (positions[0][0], positions[0][1])

    # Créer la carte
    map_ = folium.Map(location=start_location, zoom_start=12)

    # Ajouter les positions en tant que marqueurs
    for idx, (lat, lon, speed) in enumerate(positions):
        popup_text = f"Position {idx + 1}<br>Latitude: {lat:.6f}<br>Longitude: {lon:.6f}<br>Vitesse: {speed:.2f} km/h"
        folium.Marker(location=(lat, lon), popup=popup_text).add_to(map_)

    # Ajouter une ligne reliant les points
    folium.PolyLine([(lat, lon) for lat, lon, _ in positions], color="blue", weight=2.5).add_to(map_)

    # Ajouter un popup pour les résultats globaux
    folium.Marker(
        location=start_location,
        popup=f"<b>Distance totale :</b> {total_distance:.2f} km<br><b>Vitesse moyenne :</b> {average_speed:.2f} km/h",
        icon=folium.Icon(color="green", icon="info-sign")
    ).add_to(map_)

    # Sauvegarde de la carte
    output_file = "resultats_carte.html"
    map_.save(output_file)

    print(f"La carte a été générée dans le fichier {output_file}.")
else:
    print("Aucune position valide trouvée dans le fichier NMEA.")
