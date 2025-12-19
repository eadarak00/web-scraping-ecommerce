from bs4 import BeautifulSoup
from datetime import datetime
from utils import nettoyer_prix, recuperer_page,determiner_categorie, MAX_PAGES


def extraire_manojia(html, url):
    """
    Extrait les produits depuis Manojia avec gestion de la pagination
    """
    produits = []
    categorie = determiner_categorie(url)
    page = 1

    while page <= MAX_PAGES:
        # Construction de l'URL de la page
        if page == 1:
            page_url = url
        else:
            # Ajouter /page/{num} à l'URL
            page_url = url.rstrip('/') + f"/page/{page}"

        print(f"  → Page {page} : {page_url}")
        page_html = recuperer_page(page_url)
        if not page_html:
            break

        soup = BeautifulSoup(page_html, "html.parser")
        produits_tag = soup.find_all("div", class_="product")

        # Arrêt automatique si plus de produits
        if not produits_tag:
            print("[X] Plus de produits, arrêt de la pagination")
            break

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

        page += 1

    return produits
