import csv
import os
import re
from datetime import datetime
from bs4 import BeautifulSoup
import requests
from requests.exceptions import RequestException
from tqdm import tqdm

# CONFIGURATION ET UTILITAIRES

TIMEOUT = 15
MAX_PAGES = 10

# Création d'une session globale
session = requests.Session()

# Headers pour éviter le blocage
session.headers.update({
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "fr-FR,fr;q=0.9",
})


def recuperer_page(url):
    """
    Récupère le HTML d'une page via une session persistante
    """
    try:
        response = session.get(url, timeout=TIMEOUT)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"[ERREUR HTTP] {url}")
        print(e)
        return None


def determiner_categorie(url):
    """
    Détermine la catégorie Manojia à partir de l'URL
    """
    url = url.lower()
    if "electronique" in url or "informatique" in url or "multimedia" in url:
        return "multimedia"
    if "electromenagers" in url or "électroménagers" in url or "electromenager" in url:
        return "electromenager"
    return "autre"


# EXTRACTEURS PAR SITE

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
                prix = prix_tag.get_text(strip=True) if prix_tag else None

                produits.append({
                    "nom": nom,
                    "prix": prix,
                    "categorie": categorie,
                    "vendeur": "Manojia",
                    "date_collection": datetime.now()
                })

            except Exception as error:
                print("[ERREUR] Problème lors de l'extraction Manojia")
                print(error)

        page += 1

    return produits


def extraire_jumia(html, url):
    """
    Scraping Jumia avec pagination ?page=num#catalog-listing
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
                prix = prix_tag.get_text(strip=True) if prix_tag else None

                produits.append({
                    "nom": nom,
                    "prix": prix,
                    "categorie": categorie,
                    "vendeur": "Jumia",
                    "date_collection": datetime.now()
                })
            except Exception as error:
                print("[ERREUR] Jumia :", error)

        page += 1

    return produits

def extraire_jumia_electromenager(html, url):
    """
    Scraping Jumia avec pagination ?page=num#catalog-listing
    """
    produits = []
    categorie = determiner_categorie(url)

    base_url = url.split("?")[0]  # enlever toute query existante
    page = 1

    while page <= 30:
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
                prix = prix_tag.get_text(strip=True) if prix_tag else None

                produits.append({
                    "nom": nom,
                    "prix": prix,
                    "categorie": categorie,
                    "vendeur": "Jumia",
                    "date_collection": datetime.now()
                })
            except Exception as error:
                print("[ERREUR] Jumia :", error)

        page += 1

    return produits


def extraire_expat_dakar(html, url):
    """
    Extraction des produits depuis Expat-Dakar avec pagination automatique
    """
    produits = []
    categorie = determiner_categorie(url)

    page = 1

    while page <= 30:
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
                prix = prix_tag.get_text(strip=True) if prix_tag else None

                if nom and prix:
                    produits.append({
                        "nom": nom,
                        "prix": prix,
                        "categorie": categorie,
                        "vendeur": "Expat-Dakar",
                        "date_collection": datetime.now()
                    })

            except Exception as error:
                print("[ERREUR] Problème lors de l'extraction Expat-Dakar")
                print(error)

        page += 1

    return produits


# CONFIGURATION DES SITES À SCRAPER

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
    "jumia": {
        "url": "https://www.jumia.sn/maison-bureau-electromenager/",
        "extract": extraire_jumia_electromenager
    },
    "jumia-informatique": {
        "url": "https://www.jumia.sn/ordinateurs-accessoires-informatique/",
        "extract": extraire_jumia
    }
}


# FONCTION PRINCIPALE

def main():
    tous_les_produits = []

    # Barre de progression globale (sites)
    for site, config in tqdm(SITES.items(),
                             desc="Scraping des sites",
                             unit="site"):
        print(f"\nScraping {site}...")

        html = recuperer_page(config["url"])
        if not html:
            print("  [X] Page inaccessible")
            continue

        produits = config["extract"](html, config["url"])
        tous_les_produits.extend(produits)

        print(f"[v] {len(produits)} produits récupérés")

    # Création du dossier data
    dossier_data = "data"
    os.makedirs(dossier_data, exist_ok=True)

    # Sauvegarde en CSV
    champs = ["nom", "prix", "categorie", "vendeur", "date_collection"]

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

    print("\nExtraction terminée")
    print(f"[v] Total produits : {len(tous_les_produits)}")
    print("[v] Fichier créé : data/produits.csv")


if __name__ == "__main__":
    main()