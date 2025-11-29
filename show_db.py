import sqlite3
from prettytable import PrettyTable

DB_PATH = "sentiment.db"   # Chemin de ta base

def show_tables(cursor):
    print("\n=== Tables disponibles ===")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    for t in tables:
        print("  -", t[0])


def show_predictions(cursor):
    print("\n=== Contenu de la table predictions ===")
    cursor.execute("SELECT * FROM predictions")
    rows = cursor.fetchall()

    if not rows:
        print("⚠ La table est vide.")
        return

    # Table formatée
    table = PrettyTable()
    table.field_names = ["id", "text", "sentiment", "confidence", "date"]

    for r in rows:
        table.add_row(r)

    print(table)

    print(f"\nTotal lignes : {len(rows)}")


def main():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        print(f"Base connectée : {DB_PATH}")

        show_tables(cursor)
        show_predictions(cursor)

    except Exception as e:
        print("❌ Erreur :", e)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
