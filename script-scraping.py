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

def main():
    """
    Fonction principale pour tester fetch_page avec différents cas.
    """
    print("=== Test de la fonction fetch_page ===\n")

    # Liste d'URLs à tester (incluant des cas valides et invalides)
    test_urls = [
        "https://www.manojia.com/product-category/electromenagers/",  # Site valide
        "https://www.manojia.com/product-category/electronique/",  # Site valide
        "https://www.manojia.com/product-category/electronique/2211",  # Retourne 200
        "https://www.manojia.com/product-category/electromenagers/404",
    ]

    for url in test_urls:
        print(f"[TEST] : {url}")

        html = fetch_page(url)

        if html:
            print(f"[SUCCESS] Page récupérée  ({len(html)} caractères)\n")
        else:
            print(f"[ECHEC] Échec de la récupération\n")


if __name__ == "__main__":
    main()