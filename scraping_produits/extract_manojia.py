from bs4 import BeautifulSoup
from datetime import datetime
from utils import  nettoyer_prix

def extraire_manojia_produits(html):
    produits = []
    soup = BeautifulSoup(html, 'html.parser')
    produits_tag = soup.find_all('div', class_='product')

    for produit in produits_tag:
        try:
            nom = produit.find("h3", class_='product-title').get_text(strip=True)
            prix_tag = produit.find("span", class_="price")
            prix_brut = prix_tag.get_text(strip=True) if prix_tag else None
            prix = nettoyer_prix(prix_brut)

            produits.append({
                'nom': nom,
                'prix': prix,
                'vendeur': 'Manojia',
                'date': datetime.now().isoformat(),
            })
        except Exception as e:
            print("[ERREUR] Problème lors du parsing d’un produit")
            print(e)
    return produits