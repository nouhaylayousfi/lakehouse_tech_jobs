import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()
load_dotenv()
print("CLIENT_ID:", os.getenv("FT_CLIENT_ID"))
print("CLIENT_SECRET:", os.getenv("FT_CLIENT_SECRET"))

# 1. Obtenir le token
token_response = requests.post(
    "https://entreprise.francetravail.fr/connexion/oauth2/access_token?realm=%2Fpartenaire",
    data={
        "grant_type":    "client_credentials",
        "client_id":     os.getenv("FT_CLIENT_ID"),
        "client_secret": os.getenv("FT_CLIENT_SECRET"),
        "scope":         "api_offresdemploiv2 o2dsoffre",
    },
    headers={"Content-Type": "application/x-www-form-urlencoded"},
)
print(token_response.status_code)
print(token_response.json())
token = token_response.json()["access_token"]


# 2. Récupérer UNE seule offre
response = requests.get(
    "https://api.francetravail.io/partenaire/offresdemploi/v2/offres/search",
    headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
    params={"motsCles": "data engineer", "range": "0-0"},
)

# 3. Afficher la réponse brute complète
data = response.json()
print(json.dumps(data, indent=2, ensure_ascii=False))