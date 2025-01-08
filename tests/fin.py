import re  # Importation du module pour les expressions régulières
from math import radians, sin, cos, sqrt, atan2  # Importation de fonctions mathématiques pour les calculs de distances GPS

# Fonction pour convertir les coordonnées NMEA (format ddmm.mmmm) en degrés décimaux
def nmea_to_decimal(coord, direction):
    degrees = int(coord[:2])  # Extraire les deux premiers caractères pour les degrés
    minutes = float(coord[2:])  # Le reste représente les minutes
    decimal = degrees + (minutes / 60)  # Conversion en degrés décimaux
    if direction in ['S', 'W']:  # Si la direction est sud ou ouest, la coordonnée est négative
        decimal *= -1
    return decimal  # Retourne la coordonnée en degrés décimaux

# Fonction pour calculer la distance entre deux points GPS (utilisant la formule de Haversine)
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Rayon moyen de la Terre en kilomètres
    dlat = radians(lat2 - lat1)  # Différence de latitude en radians
    dlon = radians(lon2 - lon1)  # Différence de longitude en radians
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2  # Formule de Haversine
    c = 2 * atan2(sqrt(a), sqrt(1 - a))  # Calcul de l'angle central
    return R * c  # Retourne la distance en kilomètres

# Liste pour stocker les positions GPS (latitude, longitude, vitesse)
positions = []

# Lecture du fichier contenant les trames NMEA
with open("trames.nmea", "r") as file:  # Ouvre le fichier en mode lecture
    for line in file:  # Parcourt chaque ligne du fichier
        if line.startswith("$GPRMC"):  # Vérifie si la ligne est une trame GPRMC
            fields = line.split(",")  # Divise la ligne en champs séparés par des virgules
            if fields[2] == "A":  # Vérifie si le statut est actif ('A')
                lat = nmea_to_decimal(fields[3], fields[4])  # Convertit la latitude en degrés décimaux
                lon = nmea_to_decimal(fields[5], fields[6])  # Convertit la longitude en degrés décimaux
                speed = float(fields[7]) * 1.852  # Convertit la vitesse de nœuds en km/h
                positions.append((lat, lon, speed))  # Ajoute les données (latitude, longitude, vitesse) à la liste

# Calcul de la distance totale parcourue
total_distance = 0  # Initialisation de la distance totale
for i in range(1, len(positions)):  # Parcourt toutes les positions GPS, sauf la première
    # Ajoute la distance entre deux positions consécutives à la distance totale
    total_distance += haversine(positions[i - 1][0], positions[i - 1][1], positions[i][0], positions[i][1])

# Calcul de la vitesse moyenne
average_speed = sum(p[2] for p in positions) / len(positions)  # Moyenne des vitesses enregistrées

# Génération de la page HTML contenant la carte
html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">  <!-- Encodage des caractères -->
    <meta name="viewport" content="width=device-width, initial-scale=1.0">  <!-- Compatibilité mobile -->
    <title>Carte GPS NMEA</title>  <!-- Titre de la page -->
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />  <!-- Feuille de style Leaflet -->
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>  <!-- Bibliothèque JavaScript Leaflet -->
    <style>
        body {{
            font-family: Arial, sans-serif;  /* Police par défaut */
            margin: 20px;
        }}
        #map {{
            height: 600px;  /* Hauteur de la carte */
            width: 100%;  /* Largeur de la carte */
            margin: 20px auto;  /* Centrer la carte avec des marges */
        }}
    </style>
</head>
<body>
    <h1>Carte des positions GPS</h1>
    <p><strong>Distance totale parcourue :</strong> {total_distance:.2f} km</p>  <!-- Affiche la distance totale -->
    <p><strong>Vitesse moyenne :</strong> {average_speed:.2f} km/h</p>  <!-- Affiche la vitesse moyenne -->
    <div id="map"></div>  <!-- Div où la carte sera affichée -->
    <script>
        // Initialisation de la carte
        var map = L.map('map').setView([{positions[0][0]:.6f}, {positions[0][1]:.6f}], 13);  // Centrer la carte sur la première position avec un zoom

        // Ajouter les tuiles OpenStreetMap
        L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
            attribution: '© OpenStreetMap contributors'  // Attribution des données de la carte
        }}).addTo(map);

        // Ajouter les positions sur la carte
"""
for lat, lon, speed in positions:  # Parcourt toutes les positions GPS
    html_content += f"""
        L.marker([{lat:.6f}, {lon:.6f}]).addTo(map)  // Ajoute un marqueur pour chaque position
            .bindPopup("Vitesse : {speed:.2f} km/h");  // Affiche la vitesse dans une popup
    """
html_content += """
    </script>
</body>
</html>
"""

# Sauvegarde du fichier HTML
output_file = "carte.html"  # Nom du fichier de sortie
with open(output_file, "w") as file:  # Ouvre le fichier en écriture
    file.write(html_content)  # Écrit le contenu HTML dans le fichier

# Message de confirmation
print(f"La carte a été générée dans le fichier {output_file}.")