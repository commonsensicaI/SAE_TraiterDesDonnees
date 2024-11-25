import re
import geopy.distance

def analyser_trame(fichier):
    positions = []
    with open(fichier, 'r') as file:
        for line in file:
            if line.startswith('$GPGGA'):  # Exemple de trame NMEA
                data = line.split(',')
                lat = float(data[2]) if data[2] else None
                lon = float(data[4]) if data[4] else None
                altitude = float(data[9]) if data[9] else None
                positions.append((lat, lon, altitude))

    calculs = calculer_metrques(positions)
    return positions, calculs

def calculer_metrques(positions):
    max_lat = max(positions, key=lambda x: x[0])
    min_lat = min(positions, key=lambda x: x[0])
    max_lon = max(positions, key=lambda x: x[1])
    min_lon = min(positions, key=lambda x: x[1])

    distance = 0
    for i in range(1, len(positions)):
        distance += geopy.distance.distance(positions[i-1][:2], positions[i][:2]).km

    return {
        'max_lat': max_lat,
        'min_lat': min_lat,
        'max_lon': max_lon,
        'min_lon': min_lon,
        'distance': distance,
    }

def generer_page_web(positions, calculs, output_dir):
    # Générer une page HTML simple pour afficher la carte et les résultats
    html_content = f"""
    <html>
    <head>
        <title>Analyse des Trames GPS</title>
        <link rel="stylesheet" href="../css/style.css">
    </head>
    <body>
        <h1>Analyse des Trames GPS</h1>
        <div>
            <h2>Positions</h2>
            <ul>
    """
    
    for lat, lon, alt in positions:
        html_content += f"<li>Lat: {lat}, Lon: {lon}, Alt: {alt}</li>"
    
    html_content += f"""
        </ul>
        <h2>Calculs</h2>
        <p>Position la plus au nord: {calculs['max_lat']}</p>
        <p>Position la plus au sud: {calculs['min_lat']}</p>
        <p>Position la plus à l'est: {calculs['max_lon']}</p>
        <p>Position la plus à l'ouest: {calculs['min_lon']}</p>
        <p>Distance totale parcourue: {calculs['distance']} km</p>
    </body>
    </html>
    """
    
    with open(f"{output_dir}/index.html", "w") as f:
        f.write(html_content)
