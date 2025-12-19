import csv
import os
from utils import recuperer_page
from extract_manojia import extraire_manojia_produits
from extract_expat_dakar import extraire_expat_dakar
from extract_dakarmarket import extraire_dakarmarket

SITES = {
    "manojia": {
        "url": "https://www.manojia.com/product-category/electronique",
        "extract": extraire_manojia_produits
    },
    "expat-dakar": {
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
            produits = config["extract"](html)
            tous_les_produits.extend(produits)
            print(f"{len(produits)} produits récupérés")

    # Création du dossier data à la racine
    dossier_data = "/home/eadarak/projets/web-scraping-ecommerce/data"
    os.makedirs(dossier_data, exist_ok=True)

    # Champs CSV cohérents avec les dictionnaires extraits
    champs = ["nom", "prix", "vendeur", "date_collection"]

    # Sauvegarde CSV
    with open(f"{dossier_data}/produits.csv", "w", newline="", encoding="utf-8") as fichier:
        writer = csv.DictWriter(fichier, fieldnames=champs)
        writer.writeheader()
        writer.writerows(tous_les_produits)

    print("Extraction terminée. Fichier créé dans 'data/produits.csv'")

if __name__ == "__main__":
    main()
