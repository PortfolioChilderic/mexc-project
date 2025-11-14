import time
import hmac
import hashlib
import csv
import os
from urllib.parse import urlencode

import requests

# 👉 Mets tes clés dans des variables d'environnement de ton système
API_KEY = os.getenv("MEXC_API_KEY")
API_SECRET = os.getenv("MEXC_API_SECRET")

BASE_URL = "https://api.mexc.co"

if not API_KEY or not API_SECRET:
    raise RuntimeError("Tu dois définir MEXC_API_KEY et MEXC_API_SECRET dans tes variables d'environnement")

def sign_params(params: dict) -> dict:
    """
    Ajoute la signature HMAC SHA256 aux paramètres pour les endpoints SIGNED.
    Doc MEXC : signature = HMAC_SHA256(secretKey, totalParams) :contentReference[oaicite:1]{index=1}
    """
    query_string = urlencode(params)
    signature = hmac.new(
        API_SECRET.encode("utf-8"),
        query_string.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()
    params["signature"] = signature
    return params

def signed_get(path: str, params: dict):
    """
    Envoie une requête GET signée sur l'API MEXC.
    """
    url = BASE_URL + path
    params["timestamp"] = int(time.time() * 1000)
    params = sign_params(params)

    headers = {
        "X-MEXC-APIKEY": API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers, params=params, timeout=10)
    if not response.ok:
        raise RuntimeError(f"Erreur API {response.status_code}: {response.text}")
    return response.json()

def export_account_balances_to_csv(csv_filename: str = "mexc_balances.csv"):
    """
    Récupère les infos de compte (Spot) et exporte les balances dans un CSV.
    Utilise l'endpoint GET /api/v3/account :contentReference[oaicite:2]{index=2}
    """
    print("Récupération des informations de compte...")
    data = signed_get("/api/v3/account", params={})

    balances = data.get("balances", [])
    if not balances:
        print("Aucune balance retournée par l'API.")
        return

    print(f"{len(balances)} assets trouvés, écriture dans {csv_filename} ...")

    with open(csv_filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["asset", "free", "locked", "available"])

        for b in balances:
            writer.writerow([
                b.get("asset"),
                b.get("free"),
                b.get("locked"),
                b.get("available")
            ])

    print(f"✅ Export terminé : {csv_filename}")

if __name__ == "__main__":
    export_account_balances_to_csv()
