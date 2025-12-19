from bs4 import BeautifulSoup
from datetime import datetime
from utils import nettoyer_prix

def extraire_expat_dakar(html):
    """
    Extraction des produits depuis Expat-Dakar
    """
    produits = []

    if html is None:
        return produits

    soup = BeautifulSoup(html, "html.parser")
    produits_tag = soup.find_all("div", class_="cars-listing-card")

    for produit in produits_tag:
        try:
            titre_tag = produit.find("div", class_="cars-listing-card__header__title")
            nom = titre_tag.get_text(strip=True) if titre_tag else None

            prix_tag = produit.find("span", class_="cars-listing-card__price__value")
            prix_brut = prix_tag.get_text(strip=True) if prix_tag else None
            prix = nettoyer_prix(prix_brut)

            produits.append({
                'nom': nom,
                'prix': prix,
                'vendeur': 'Expat-Dakar',
                'date_collection': datetime.now().isoformat(),
            })

        except Exception as error:
            print("[ERREUR] Problème lors de l'extraction Expat-Dakar")
            print(error)

    return produits
