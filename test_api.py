import requests

# URL de ton API Flask
url = "http://127.0.0.1:5000/predict"

# Liste de phrases à tester
texts = [
    "J'adore ce produit !",
    "Ce film etait vraiment nul...",
    "Je ne sais pas trop quoi penser de ce service",
    "Le temps est magnifique aujourd'hui"
]

# Boucle sur chaque phrase
for text in texts:
    response = requests.post(url, json={"text": text})
    
    if response.status_code == 200:
        result = response.json()
        print(f"Texte original : {result['original_text']}")
        print(f"Texte corrigé : {result['corrected_text']}")
        print(f"Sentiment : {result['label']} (score : {result['score']})")
        print("-" * 50)
    else:
        print(f"Erreur pour '{text}' :", response.status_code, response.text)
