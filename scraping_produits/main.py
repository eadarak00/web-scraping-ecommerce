import csv
import os
from tqdm import tqdm

from utils import recuperer_page
from extract_manojia import extraire_manojia
from extract_expat_dakar import extraire_expat_dakar
from extract_jumia import extraire_jumia


SITES = {
    "manojia": {
        "url": "https://www.manojia.com/product-category/informatique",
        "extract": extraire_manojia
    },
    "manojia-multimedia": {
        "url": "https://www.manojia.com/product-category/electronique",
        "extract": extraire_manojia
    },
    "manojia-electromenagers": {
        "url": "https://www.manojia.com/product-category/electromenagers",
        "extract": extraire_manojia
    },
    "expat-multimedia": {
        "url": "https://www.expat-dakar.com/multimedia",
        "extract": extraire_expat_dakar
    },
    "jumia": {
        "url": "https://www.jumia.sn/maison-bureau-electromenager/",
        "extract": extraire_jumia
    },
    "jumia-informatique": {
        "url": "https://www.jumia.sn/ordinateurs-accessoires-informatique/",
        "extract": extraire_jumia
    }
}


def main():
    tous_les_produits = []

    # Barre de progression globale (sites)
    for site, config in tqdm(SITES.items(),
                             desc="Scraping des sites",
                             unit="site"):
        print(f"\nScraping {site}...")

        html = recuperer_page(config["url"])
        if not html:
            print("  [X] Page inaccessible")
            continue

        produits = config["extract"](html, config["url"])
        tous_les_produits.extend(produits)

        print(f"[v] {len(produits)} produits récupérés")

    # Dossier data à la racine du projet
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    BASE_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
    dossier_data = os.path.join(BASE_DIR, "data")

    os.makedirs(dossier_data, exist_ok=True)

    champs = ["nom", "prix", "categorie", "vendeur", "date_collection"]

    with open(os.path.join(dossier_data, "produits.csv"),
              "w",
              newline="",
              encoding="utf-8") as fichier:
        writer = csv.DictWriter(
            fichier,
            fieldnames=champs,
            extrasaction="ignore"
        )
        writer.writeheader()
        writer.writerows(tous_les_produits)

    print("\nExtraction terminée")
    print(f"[v] Total produits : {len(tous_les_produits)}")
    print("[v] Fichier créé : data/produits.csv")


if __name__ == "__main__":
    main()
