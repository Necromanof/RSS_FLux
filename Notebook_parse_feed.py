import feedparser
import concurrent.futures
import logging
import time

# Implémentation des logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Chargement des flux RSS
def charger_flux(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        logging.error(f"Fichier non trouvé : {path}")
        return []

# Chargement des mots-clés
def charger_mots_cles(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return [mot.strip().lower() for mot in f if mot.strip()]
    except FileNotFoundError:
        logging.error(f"Fichier non trouvé : {path}")
        return []

# Analyse d'un flux RSS
def analyser_flux(url, mots_cles):
    resultats = []
    try:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            titre = entry.get("title", "")
            description = entry.get("summary", "")
            date = entry.get("published", "none")
            lien = entry.get("link", "none")

            contenu = f"{titre} {description}".lower()
            for mot in mots_cles:
                if mot in contenu:
                    logging.info(f"J'ai trouvé le mot: '{mot}' dans cet article : {titre}")
                    resultats.append({
                        "titre": titre,
                        "date": date,
                        "url": lien,
                        "mot_cle": mot
                    })
                    break
    except Exception as e:
        logging.warning(f"Erreur lors de l'analyse de {url} : {e}")
    return resultats

# Fonction principale
def main():
    start_time = time.time()
    rss_list = charger_flux("rss_list.txt")
    mots_cles = charger_mots_cles("mots_cles.txt")
    tous_les_resultats = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(analyser_flux, url, mots_cles): url for url in rss_list}
        for future in concurrent.futures.as_completed(futures):
            resultats = future.result()
            tous_les_resultats.extend(resultats)

    with open("resultat.txt", "w", encoding="utf-8") as f:
        for res in tous_les_resultats:
            ligne = f"{res['titre']} | {res['date']} | {res['url']} | Mot-clé : {res['mot_cle']}"
            print(ligne)
            f.write(ligne + "\n")

    end_time = time.time()
    execution_time = end_time - start_time
    logging.info(f"Temps d'exécution : {execution_time:.2f} secondes")
    logging.info(f"Nombre total de résultats : {len(tous_les_resultats)}")

if __name__ == "__main__":
    main()