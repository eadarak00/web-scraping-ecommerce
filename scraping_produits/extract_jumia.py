from bs4 import BeautifulSoup
from datetime import datetime
from utils import nettoyer_prix, recuperer_page, MAX_PAGES, determiner_categorie


def extraire_jumia(html, url):
    """
    Scraping Jumia avec pagination `?page=num#catalog-listing`
    """
    produits = []
    categorie = determiner_categorie(url)

    base_url = url.split("?")[0]  # enlever toute query existante
    page = 1

    while page <= MAX_PAGES:
        # Construire l'URL paginée
        if page == 1:
            page_url = base_url
        else:
            page_url = f"{base_url}?page={page}#catalog-listing"

        print(f"  → Jumia page {page} : {page_url}")

        page_html = recuperer_page(page_url)
        if not page_html:
            break

        soup = BeautifulSoup(page_html, "html.parser")
        produits_tag = soup.find_all("article", class_="prd")

        if not produits_tag:
            print("[X] Plus de produits Jumia, arrêt pagination")
            break

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
                print("[ERREUR] Jumia :", error)

        page += 1

    return produits
