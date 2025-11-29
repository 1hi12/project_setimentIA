import requests
import json
import time

BASE_URL = "http://127.0.0.1:5000"

# ------------------------------
# Fonction : envoyer une phrase
# ------------------------------
def test_predict(text):
    url = f"{BASE_URL}/predict"
    payload = {"text": text}

    print("\n🟦 Envoi :", text)

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
    except Exception as e:
        print("❌ Erreur:", e)
        return

    data = response.json()

    print("⬇️ Réponse reçue :")
    print(json.dumps(data, indent=4, ensure_ascii=False))


# ------------------------------
# Fonction : tester les stats
# ------------------------------
def test_stats():
    url = f"{BASE_URL}/stats"
    print("\n📊 Lecture des stats...")

    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as e:
        print("❌ Erreur stats:", e)
        return

    print(json.dumps(response.json(), indent=4, ensure_ascii=False))


# ------------------------------
# Programme principal
# ------------------------------
if __name__ == "__main__":

    tests = [
        "this product is bad",
        "i like this shop very goood",
        "domage",
        "why? sales are down",
        "satisaite de cette magasin"
    ]

    for text in tests:
        test_predict(text)
        time.sleep(1)   # Pause légère pour éviter surcharge backend

    test_stats()

    print("\n✅ Test terminé !")
