.. TrameGPS documentation master file, created by
   sphinx-quickstart on Tue Jan 7 19:49:51 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

D'accord, voici tout le code `.rst` prêt à être copié. Tu n'as qu'à coller directement dans ton fichier `index.rst` :

```rst
TrameGPS documentation
======================

Ce projet permet de traiter les données GPS extraites des trames NMEA pour calculer la distance parcourue et la vitesse moyenne. Il génère également une carte interactive à partir des données collectées.

Fonctionnalités principales
---------------------------
- **Conversion des coordonnées GPS** : Conversion des coordonnées NMEA (format ddmm.mmmm) en degrés décimaux.
- **Calcul de la distance parcourue** : Utilisation de la formule de Haversine pour calculer la distance entre deux points GPS.
- **Vitesse moyenne** : Calcul de la vitesse moyenne à partir des vitesses enregistrées dans les trames.
- **Carte interactive** : Génération d'une carte utilisant Leaflet pour afficher les positions GPS et les vitesses correspondantes.

Installation
------------
1. Clonez le dépôt ou téléchargez les fichiers du projet.
2. Assurez-vous d'avoir Python installé.
3. Installez les dépendances nécessaires en utilisant la commande suivante :

   ```bash
   pip install -r requirements.txt
   ```

Utilisation
-----------
1. Placez vos fichiers de trames NMEA dans le dossier `data/`.
2. Exécutez le script `trameGPS.py` pour analyser les trames et générer les résultats.
3. Les positions et vitesses seront affichées dans une carte interactive.

Exemple de code Python
-----------------------

Voici un exemple de code Python pour traiter les trames NMEA :

```python
import math

def nmea_to_decimal(coord, direction):
    """Convertit les coordonnées NMEA en degrés décimaux."""
    degrees = int(coord[:2])
    minutes = float(coord[2:])
    decimal = degrees + (minutes / 60)

    if direction in ['S', 'W']:
        decimal = -decimal
    return decimal

def calculer_distance(lat1, lon1, lat2, lon2):
    """Calcule la distance entre deux points GPS en utilisant la formule de Haversine."""
    R = 6371  # Rayon de la Terre en km
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c  # Distance en km
    return distance

# Exemple d'utilisation
positions = []
with open("data/trames.nmea", "r") as file:
    for line in file:
        if line.startswith("$GPRMC"):
            fields = line.split(",")
            if fields[2] == "A":
                lat = nmea_to_decimal(fields[3], fields[4])
                lon = nmea_to_decimal(fields[5], fields[6])
                speed = float(fields[7]) * 1.852  # Conversion de la vitesse en km/h
                positions.append((lat, lon, speed))

# Calcul de la distance totale parcourue
distance_totale = 0
for i in range(1, len(positions)):
    lat1, lon1, _ = positions[i - 1]
    lat2, lon2, _ = positions[i]
    distance_totale += calculer_distance(lat1, lon1, lat2, lon2)

print(f"Distance totale parcourue: {distance_totale:.2f} km")
```

Explication du code
--------------------
1. **Fonction `nmea_to_decimal`** : Cette fonction convertit les coordonnées NMEA en degrés décimaux. Elle prend en entrée la coordonnée et la direction (N/S ou E/O).
2. **Fonction `calculer_distance`** : Utilise la formule de Haversine pour calculer la distance entre deux points GPS en kilomètres.
3. **Lecture des trames NMEA** : Le code lit chaque ligne du fichier `trames.nmea`, extrait les coordonnées GPS et les vitesses.
4. **Calcul de la distance totale** : Une fois les positions extraites, le code calcule la distance totale parcourue en additionnant les distances entre chaque point.

Carte interactive
-----------------
Pour afficher les positions GPS sur une carte, vous pouvez utiliser la bibliothèque `folium`. Voici un exemple de code pour générer une carte interactive :

```python
import folium

# Créer une carte centrée sur la première position
map = folium.Map(location=[positions[0][0], positions[0][1]], zoom_start=12)

# Ajouter des marqueurs pour chaque position
for pos in positions:
    folium.Marker([pos[0], pos[1]], popup=f"Vitesse: {pos[2]:.2f} km/h").add_to(map)

# Sauvegarder la carte en fichier HTML
map.save("carte_interactive.html")
```

Ce code génère une carte interactive avec des marqueurs pour chaque position, incluant la vitesse à chaque point. La carte est sauvegardée sous le nom `carte_interactive.html`.

Conclusion
----------
Le projet permet de traiter des trames NMEA, de calculer la distance parcourue, la vitesse moyenne, et d'afficher les données sur une carte interactive. Il utilise Python et plusieurs bibliothèques comme `math` pour les calculs et `folium` pour la visualisation. En suivant les instructions d'installation et d'utilisation, vous pourrez facilement analyser vos propres données GPS et générer des cartes.

Références
----------
- [Documentation de Sphinx](https://www.sphinx-doc.org/en/master/)
- [Folium Documentation](https://python-visualization.github.io/folium/)
```