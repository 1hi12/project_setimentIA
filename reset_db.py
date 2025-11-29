import os

if os.path.exists("sentiment.db"):
    os.remove("sentiment.db")
    print("Ancienne base supprimée !")
else:
    print("Aucune base à supprimer.")
