import argparse
from analyse_gps import analyser_trame, generer_page_web

def main():
    parser = argparse.ArgumentParser(description="Analyse des trames GPS NMEA 0183.")
    parser.add_argument('--input-file', required=True, help='Fichier contenant la trame GPS')
    parser.add_argument('--output-dir', required=True, help='Répertoire de sortie pour la page HTML')
    args = parser.parse_args()

    positions, calculs = analyser_trame(args.input_file)
    
    generer_page_web(positions, calculs, args.output_dir)

if __name__ == "__main__":
    main()