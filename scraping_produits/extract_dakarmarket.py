from bs4 import BeautifulSoup
from datetime import datetime
from utils import nettoyer_prix


def extraire_dakarmarket(html):
    """
    Extraction des produits depuis DakarMarket
    Gère les prix normaux et les prix en promotion
    """
    produits = []

    if html is None:
        return produits

    soup = BeautifulSoup(html, "html.parser")
    produits_tag = soup.find_all("div", class_="product-card")

    for produit in produits_tag:
        try:
            # ---- NOM DU PRODUIT ----
            titre_tag = produit.select_one("h5.card-title a")
            nom = titre_tag.get_text(strip=True) if titre_tag else None

            # ---- PRIX ACTUEL (priorité au prix promo) ----
            prix_tag = (
                produit.select_one("span.h5.text-danger.fw-bold")  # prix promo
                or produit.select_one("span.h5.text-primary.fw-bold")  # prix normal
            )

            prix_brut = prix_tag.get_text(strip=True) if prix_tag else None
            prix = nettoyer_prix(prix_brut)

            if nom and prix:
                produits.append({
                    "nom": nom,
                    "prix": prix,
                    "vendeur": "DakarMarket",
                    "date_collection": datetime.now().isoformat(),
                })

        except Exception as error:
            print("[ERREUR] Problème lors de l'extraction DakarMarket")
            print(error)

    return produits
