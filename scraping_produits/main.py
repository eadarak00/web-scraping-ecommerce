import csv
import os
from utils import recuperer_page
from extract_manojia import extraire_manojia
from extract_expat_dakar import extraire_expat_dakar
from extract_dakarmarket import extraire_dakarmarket


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
    "dakar-market": {
        "url": "https://dakarmarket.sn/shopping?categorie=electronique",
        "extract": extraire_dakarmarket
    }
}


def main():
    tous_les_produits = []

    for site, config in SITES.items():
        print(f"Scraping {site}...")
        html = recuperer_page(config["url"])

        if html:
            if site.startswith("expat") or site.startswith("manojia"):
                produits = config["extract"](html, config["url"])
            else:
                produits = config["extract"](html)

            tous_les_produits.extend(produits)
            print(f"{len(produits)} produits récupérés")

    # Dossier data à la racine du projet
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    BASE_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
    dossier_data = os.path.join(BASE_DIR, "data")

    os.makedirs(dossier_data, exist_ok=True)

    # Champs CSV
    champs = ["nom", "prix", "categorie", "vendeur", "date_collection"]

    # Sauvegarde CSV
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

    print("[v] Extraction terminée. Fichier créé dans 'data/produits.csv'")


if __name__ == "__main__":
    main()