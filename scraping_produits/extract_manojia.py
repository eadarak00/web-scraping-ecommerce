from bs4 import BeautifulSoup
from datetime import datetime
from utils import nettoyer_prix

def determiner_categorie(url):
    """
    Détermine la catégorie Manojia à partir de l'URL
    """
    url = url.lower()
    if "electronique" in url or "informatique" in url:
        return "multimedia"
    if "electromenagers" in url or "électroménagers" in url:
        return "electromenager"
    return "autre"

def extraire_manojia(html, url):
    """
    Extrait les produits depuis une page Manojia avec catégorie
    """
    produits = []

    if html is None:
        return produits

    categorie = determiner_categorie(url)

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
                "categorie": categorie,
                "vendeur": "Manojia",
                "date_collection": datetime.now().isoformat()
            })

        except Exception as error:
            print("[ERREUR] Problème lors de l'extraction Manojia")
            print(error)

    return produits
