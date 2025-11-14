import time
import hmac
import hashlib
import os
import requests
from urllib.parse import urlencode

# ================================
# 🔧 CONFIG GLOBALE
# ================================

# Choisis ici l'URL racine
BASE_URL = "https://api.mexc.co"
# BASE_URL = "https://api.mexc.com"   # version officielle

# Choisis l'endpoint à tester (modifiable à la volée)
API_ENDPOINT = "/api/v3/account"                    # exemple : infos de compte

# Charge les clés (optionnel si tu veux tester des endpoints publics)
API_KEY = os.getenv("MEXC_API_KEY")
API_SECRET = os.getenv("MEXC_API_SECRET")

# ================================
# 🔧 FONCTION SIGNATURE
# ================================

def sign_params(params: dict) -> dict:
    """Crée la signature nécessaire pour les endpoints SIGNED."""
    if not API_SECRET:
        raise RuntimeError("Pas de MEXC_API_SECRET dans les variables d'environnement")

    query = urlencode(params)
    signature = hmac.new(
        API_SECRET.encode(),
        query.encode(),
        hashlib.sha256
    ).hexdigest()
    params["signature"] = signature
    return params

# ================================
# 🔧 FONCTION PRINCIPALE
# ================================

def call_api(endpoint: str, signed: bool = False, extra_params: dict = None):
    """
    Teste un endpoint et retourne le JSON brut de l'API.
    - endpoint : "/api/v3/account" ou autre
    - signed   : True si l'API nécessite signature
    - extra_params : d'autres paramètres à transmettre
    """

    url = BASE_URL + endpoint
    params = extra_params or {}

    # Ajout du timestamp + signature si endpoint "SIGNED"
    if signed:
        params["timestamp"] = int(time.time() * 1000)
        params = sign_params(params)

    headers = {
        "Content-Type": "application/json",
    }

    if API_KEY:
        headers["X-MEXC-APIKEY"] = API_KEY

    print(f"\n👉 Requête envoyée à : {url}")
    print(f"👉 Paramètres : {params}")
    print(f"👉 Headers : {headers}\n")

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        print("📥 Réponse brute (status code) :", response.status_code)
        print("📥 Réponse JSON complète :\n")
        print(response.text)      # texte brut ici (json ou pas)
        print("\n✔ Test terminé.\n")

    except Exception as e:
        print("❌ Erreur lors de l'appel API :", e)


# ================================
# 🚀 TEST (modifiable)
# ================================

if __name__ == "__main__":
    # Exemple : /api/v3/account → SIGNED=True
    call_api(API_ENDPOINT, signed=True)
