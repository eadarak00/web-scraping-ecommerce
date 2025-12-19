from tkinter.tix import MAX

from bs4 import BeautifulSoup
from datetime import datetime

from utils import nettoyer_prix, recuperer_page, determiner_categorie, MAX_PAGES


def extraire_expat_dakar(html, url):
    """
    Extraction des produits depuis Expat-Dakar avec pagination automatique
    """
    produits = []
    categorie = determiner_categorie(url)

    page = 1

    while page <= MAX_PAGES:
        # Construction URL paginée
        if page == 1:
            page_url = url
        else:
            page_url = f"{url}?page={page}" if "?" not in url else f"{url}&page={page}"

        print(f"  → Page {page} : {page_url}")

        page_html = recuperer_page(page_url)
        if not page_html:
            break

        soup = BeautifulSoup(page_html, "html.parser")
        produits_tag = soup.find_all("div", class_="cars-listing-card")

        # Arrêt automatique si plus de résultats
        if not produits_tag:
            print("[X] Plus de produits, arrêt pagination")
            break

        for produit in produits_tag:
            try:
                titre_tag = produit.find(
                    "div",
                    class_="cars-listing-card__header__title"
                )
                nom = titre_tag.get_text(strip=True) if titre_tag else None

                prix_tag = produit.find(
                    "span",
                    class_="cars-listing-card__price__value"
                )
                prix_brut = prix_tag.get_text(strip=True) if prix_tag else None
                prix = nettoyer_prix(prix_brut)

                if nom and prix:
                    produits.append({
                        "nom": nom,
                        "prix": prix,
                        "categorie": categorie,
                        "vendeur": "Expat-Dakar",
                        "date_collection": datetime.now().isoformat(),
                    })

            except Exception as error:
                print("[ERREUR] Problème lors de l'extraction Expat-Dakar")
                print(error)

        page += 1

    return produits
