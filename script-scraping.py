import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
from datetime import datetime
import time
import csv
import os

# URL et Configuration
BASE_URL = "https://www.manojia.com/product-category"
TIMEOUT = 10

CATEGORIES = {
    "electromenager" : [
        f"{BASE_URL}/eletromenaelectromenagers/page/1/"
    ],
    "multimedia" : [
        f"{BASE_URL}/electronique/page/1/"
        f"{BASE_URL}/informatique/page/1/"
    ]
}

def recuperer_page(url):
    """
    Récupère le HTML d'une page web.
    """
    try:
        response = requests.get(url, timeout=TIMEOUT)
        response.raise_for_status()
        return response.text
    except RequestException as error:
        print(f"[ERREUR] Impossible de récupérer la page : {url}")
        print(error)
        return None

def nettoyer_prix(prix):
    """
    Nettoie le prix (supprime FCFA, espaces).
    """
    if not prix:
        return None

    return (
        prix.replace("FCFA","")
        .replace("F CFA", "")
        .replace(" ", "")
        .strip()
    )

def extraire_produits(html, categorie):
    """
    Extrait les produits d'une page HTML.
    """

    if html is None:
        return []

    soup = BeautifulSoup(html, "html.parser")
    produits = []

    produits_div = soup.find_all("div", class_="product")

    for produit in produits_div:
        try:
            titre_tag = produit.find("h3", class_="product-title")
            if not titre_tag:
                continue

            lien_tag = titre_tag.find("a")
            nom = lien_tag.get_text(strip=True)

            prix_tag = produit.find("span", class_="price")
            prix_brut = prix_tag.get_text(strip=True) if prix_tag else None
            prix = nettoyer_prix(prix_brut)

            produits.append({
                "nom": nom,
                "prix": prix,
                "categorie": categorie,
                "vendeur": "Manojia",
                "date_collecte": datetime.now().isoformat()
            })
        except Exception as error:
            print("[ERREUR] Problème lors du parsing d’un produit")
            print(error)

    return produits
