import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException

def fetch_page(url):
    """
     Récupère le contenu HTML d'une page web.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except RequestException as error:
        print(f"[ERREUR] impossible de recuperer la page : {error}")
        return None


def parse_produits(html):
    """
    Analyse le HTML et extrait le nom et le prix des produits
    """
    soup = BeautifulSoup(html, "html.parser")
    produits = []

    produits_div = soup.find_all("div", class_="product")

    for produit in produits_div:
        # ----- NOM -----
        titre_tag = produit.find("h3", class_="product-title")
        if not titre_tag:
            continue

        lien_tag = titre_tag.find("a")
        nom = lien_tag.get_text(strip=True)

        # ----- PRIX -----
        price_tag = produit.find("span", class_="price")
        if not price_tag:
            continue

        prix = price_tag.get_text(strip=True)

        produits.append({
            "nom": nom,
            "prix": prix
        })

    return produits



def main():
    """
    Fonction principale pour tester  avec différents cas.
    """
    print("=== Test de la fonction parse_produits ===\n")

    html = fetch_page("https://www.manojia.com/product-category/electromenagers/")
    produits = parse_produits(html)

    for p in produits:
        print(p)

if __name__ == "__main__":
    main()