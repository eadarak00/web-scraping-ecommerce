from bs4 import BeautifulSoup
from datetime import datetime
from utils import nettoyer_prix


def determiner_categorie(url):
    url = url.lower()
    if "electromenager" in url:
        return "electromenager"
    if "informatique" in url or "electronique" in url:
        return "multimedia"
    return "autre"


def extraire_jumia(html, url):
    """
    Scraping Jumia (une seule page, sans pagination)
    """
    produits = []

    if html is None:
        return produits

    categorie = determiner_categorie(url)

    soup = BeautifulSoup(html, "html.parser")
    produits_tag = soup.find_all("article", class_="prd")

    for produit in produits_tag:
        try:
            # ---- NOM ----
            nom_tag = produit.find("h3", class_="name")
            nom = nom_tag.get_text(strip=True) if nom_tag else None

            # ---- PRIX ACTUEL ----
            prix_tag = produit.find("div", class_="prc")
            prix_brut = prix_tag.get_text(strip=True) if prix_tag else None
            prix = nettoyer_prix(prix_brut)

            if nom and prix:
                produits.append({
                    "nom": nom,
                    "prix": prix,
                    "categorie": categorie,
                    "vendeur": "Jumia",
                    "date_collection": datetime.now().isoformat()
                })

        except Exception as error:
            print("[ERREUR] Problème lors de l'extraction Jumia")
            print(error)

    return produits
