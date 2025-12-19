import requests
from requests.exceptions import RequestException
import re

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
        response = session.get(url, timeout=15)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"[ERREUR HTTP] {url}")
        print(e)
        return None


def nettoyer_prix(prix):
    """
    Nettoie le prix en supprimant toutes les variantes de 'FCFA'
    et les espaces. Retourne le prix sous forme de string propre.
    Exemples supprimés : FCFA, F CFA, f cfa, F.cfa, CFA, etc.
    """
    if not prix:
        return None

    # Supprime toutes les variantes de FCFA / CFA (insensible à la casse)
    prix = re.sub(r"f?\s*[\.\-]?\s*cfa", "", prix, flags=re.IGNORECASE)

    # Supprime les espaces classiques et insécables
    prix = prix.replace("\u202f", "")  # espace insécable fine
    prix = prix.replace("\xa0", "")    # espace insécable
    prix = prix.replace(" ", "").strip()

    return prix


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