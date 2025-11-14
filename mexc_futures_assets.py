import time
import hmac
import hashlib
import json
import csv
import os
from urllib.parse import urlencode

import requests

# ================================
# 🔧 CONFIG
# ================================

# Base Futures (contrats perpétuels USDT-M)
# Si besoin tu peux adapter si MEXC fournit un autre host (ex: contract.mexc.co si ça existe un jour)
BASE_URL = "https://contract.mexc.co"

# On essaie d'abord des variables dédiées futures, sinon on retombe sur celles du Spot
API_KEY = os.getenv("MEXC_FUTURES_API_KEY") or os.getenv("MEXC_API_KEY")
API_SECRET = os.getenv("MEXC_FUTURES_API_SECRET") or os.getenv("MEXC_API_SECRET")

if not API_KEY or not API_SECRET:
    raise RuntimeError("Tu dois définir MEXC_FUTURES_API_KEY / MEXC_FUTURES_API_SECRET (ou MEXC_API_KEY / MEXC_API_SECRET).")

# ================================
# 🔐 SIGNATURE FUTURES
# ================================

def build_param_string(params: dict) -> str:
    """
    Construit le paramètre string à signer selon la doc futures :

    - GET/DELETE : paramètres business triés par ordre alphabétique, format k=v&k2=v2
    - POST : JSON string brute (on ne s'en sert pas ici pour l'instant)
    """
    if not params:
        return ""
    # Tri des clés pour GET
    items = sorted(params.items(), key=lambda x: x[0])
    return urlencode(items, doseq=True)


def sign_futures_request(param_string: str, timestamp: str) -> str:
    """
    Signature futures : HMAC_SHA256(secret, accessKey + timestamp + param_string)
    cf. doc Integration Guide.
    """
    target = API_KEY + timestamp + param_string
    signature = hmac.new(
        API_SECRET.encode("utf-8"),
        target.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()
    return signature


def futures_get(path: str, params: dict | None = None):
    """
    Envoie une requête GET signée vers l'API Futures.
    """
    url = BASE_URL + path
    params = params or {}

    # Timestamp en ms (string)
    req_time = str(int(time.time() * 1000))

    # Chaîne de paramètres à signer
    param_string = build_param_string(params)

    # Signature
    signature = sign_futures_request(param_string, req_time)

    headers = {
        "ApiKey": API_KEY,
        "Request-Time": req_time,
        "Signature": signature,
        # Optionnel : fenêtre de validité en secondes (max 60)
        "Recv-Window": "30",
        "Content-Type": "application/json",
    }

    print(f"👉 Appel GET {url}")
    print(f"👉 Params : {params}")
    print(f"👉 Headers : {headers}")

    resp = requests.get(url, params=params, headers=headers, timeout=10)

    print(f"\n📥 Status code : {resp.status_code}")
    print("📥 Réponse brute :")
    print(resp.text)
    print("------\n")

    resp.raise_for_status()
    data = resp.json()
    if not data.get("success", False):
        raise RuntimeError(f"Erreur API Futures: code={data.get('code')} message={data.get('message')}")
    return data.get("data", [])


# ================================
# 💰 EXPORT DES ACTIFS FUTURES
# ================================

def export_futures_assets_to_csv(csv_filename: str = "mexc_futures_assets.csv"):
    """
    Récupère tous les assets du portefeuille futures et les exporte dans un CSV.

    Endpoint utilisé :
    GET /api/v1/private/account/assets
    """
    print("Récupération des actifs du portefeuille Futures...")
    assets = futures_get("/api/v1/private/account/assets")

    if not assets:
        print("Aucun actif retourné sur le portefeuille Futures (data = []).")
        return

    print(f"{len(assets)} devises trouvées. Écriture dans {csv_filename}...")

    with open(csv_filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "currency",
            "positionMargin",
            "availableBalance",
            "cashBalance",
            "frozenBalance",
            "equity",
            "unrealized",
            "bonus",
            "availableCash",
            "availableOpen",
            "debtAmount",
            "contributeMarginAmount",
            "vcoinId",
        ])

        for a in assets:
            writer.writerow([
                a.get("currency"),
                a.get("positionMargin"),
                a.get("availableBalance"),
                a.get("cashBalance"),
                a.get("frozenBalance"),
                a.get("equity"),
                a.get("unrealized"),
                a.get("bonus"),
                a.get("availableCash"),
                a.get("availableOpen"),
                a.get("debtAmount"),
                a.get("contributeMarginAmount"),
                a.get("vcoinId"),
            ])

    print(f"✅ Export Futures terminé : {csv_filename}")


if __name__ == "__main__":
    # Simple : on fait l’export CSV
    export_futures_assets_to_csv()
