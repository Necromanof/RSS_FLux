import feedparser
import concurrent.futures
import logging

# Implemtation des logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Chargement des flux RSS
def charger_flux(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        logging.error(f"Fichier non trouvé : {path}")
        return []