import requests
from requests.exceptions import RequestException

TIMEOUT = 10

def recuperer_page(url):
    """Télécharge le HTML d'une page"""
    try:
        response = requests.get(url, timeout=TIMEOUT)
        response.raise_for_status()
        return response.text
    except RequestException as error:
        print(f"[ERREUR] Page inaccessible : {url}")
        print(error)
        return None

def nettoyer_prix(prix):
    """Supprime FCFA et espaces"""
    if not prix:
        return None
    return prix.replace("FCFA", "").replace("F CFA", "").replace(" ", "").strip()