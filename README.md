# 🚀 Scripts Python pour interagir avec l'API MEXC (Spot)

Ce dépôt contient deux scripts Python permettant de tester et d’utiliser l'API Spot de MEXC :

- `mexc_test.py` — pour tester n'importe quel endpoint et afficher les réponses brutes.
- `export_mexc_balances.py` — pour exporter les soldes du portefeuille Spot dans un fichier CSV.
- `mexc_futures_assets.py` — pour récupérer et exporter les actifs du portefeuille Futures dans un fichier CSV.

Ces scripts servent de base pour automatiser des opérations, analyser son portefeuille ou développer des outils autour de l'API MEXC.

---

## ⚙️ Prérequis

### Installation des dépendances Python

```bash
pip install requests
```

### Configuration des clés API MEXC

Les scripts utilisent deux variables d’environnement :

- `MEXC_API_KEY`
- `MEXC_API_SECRET`

Sous Linux / WSL :

```bash
export MEXC_API_KEY="VOTRE_CLE_API"
export MEXC_API_SECRET="VOTRE_SECRET"
```

Sous Windows (PowerShell) :
```powershell
setx MEXC_API_KEY "VOTRE_CLE_API"
setx MEXC_API_SECRET "VOTRE_SECRET"
```

⚠️ Après un setx, redémarrer le terminal  
⚠️ Ne jamais commiter vos clés API

---

## 🧪 Script : `mexc_test.py`

Ce script permet de tester n’importe quel endpoint de l’API MEXC.

Il affiche :
- l’URL appelée
- les paramètres
- les headers
- le code HTTP
- la réponse brute (texte ou JSON)

Exécution :
python3 mexc_test.py

Pour tester un autre endpoint, modifier la valeur de `API_ENDPOINT` dans le script.

---

## 📤 Script : `export_mexc_balances.py`

Ce script interroge :
GET /api/v3/account

Il récupère les soldes du portefeuille Spot (USDT, BTC, ETH, etc.)  
Puis génère un fichier :
mexc_balances.csv

Exécution :
python3 export_mexc_balances.py

---

## 📝 Spot vs Fiat sur MEXC

Le portefeuille Spot est le seul visible via l’API Spot.

Les fonds dans :
- Fiat (EUR, USD…)
- Futures
- Earn / Savings
- Margin
- ETF

ne sont pas visibles via /api/v3/account.

Si l’API renvoie `balances: []`, vos fonds sont probablement dans Fiat.  
Il faut transférer les fonds Fiat → Spot pour qu’ils deviennent visibles via l’API.

---

## 📚 Documentation officielle

https://www.mexc.com/api-docs/spot-v3
