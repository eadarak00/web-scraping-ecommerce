from bs4 import BeautifulSoup
from datetime import datetime
from utils import nettoyer_prix


def extraire_manojia_produits(html):
    """
    Extrait les produits depuis une page Manojia
    """
    produits = []

    if html is None:
        return produits

    soup = BeautifulSoup(html, "html.parser")
    produits_tag = soup.find_all("div", class_="product")

    for produit in produits_tag:
        try:
            titre_tag = produit.find("h3", class_="product-title")
            if not titre_tag:
                continue
            nom = titre_tag.get_text(strip=True)

            prix_tag = produit.find("span", class_="price")
            prix_brut = prix_tag.get_text(strip=True) if prix_tag else None
            prix = nettoyer_prix(prix_brut)

            produits.append({
                "nom": nom,
                "prix": prix,
                "vendeur": "Manojia",
                "date_collection": datetime.now().isoformat()
            })

        except Exception as error:
            print("[ERREUR] Problème lors de l'extraction Manojia")
            print(error)

    return produits
