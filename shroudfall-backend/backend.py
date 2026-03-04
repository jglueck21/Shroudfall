import sqlite3
import json
from typing import List, Dict
import PyPDF2

DB_PATH = "database/shroudfall.db"
CONFIG_PATH = "config.json"

def get_connection():
    return sqlite3.connect(DB_PATH)

def load_armies() -> List[Dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM armies")
    armies = cursor.fetchall()
    conn.close()
    return [{"id": a[0], "name": a[1], "faction": a[2], "max_points": a[3], "total_points": a[4]} for a in armies]


def add_unit(army_id: int, unit_id: int, count: int):
    conn = get_connection()
    cursor = conn.cursor()

    # Prüfen, ob Einheit schon existiert
    cursor.execute("""
        SELECT count FROM army_units WHERE army_id=? AND unit_id=?
    """, (army_id, unit_id))
    row = cursor.fetchone()

    if row:
        cursor.execute("""
            UPDATE army_units SET count = count + ?
            WHERE army_id=? AND unit_id=?
        """, (count, army_id, unit_id))
    else:
        cursor.execute("""
            INSERT INTO army_units (army_id, unit_id, count)
            VALUES (?, ?, ?)
        """, (army_id, unit_id, count))

    conn.commit()

    # Validierung nach Hinzufügen
    if not validate_army(army_id):
        print("Ungültige Armee – Änderung wird rückgängig gemacht.")
        if row:
            cursor.execute("""
                UPDATE army_units SET count = count - ?
                WHERE army_id=? AND unit_id=?
            """, (count, army_id, unit_id))
        else:
            cursor.execute("""
                DELETE FROM army_units WHERE army_id=? AND unit_id=?
            """, (army_id, unit_id))
        conn.commit()

    conn.close()

def remove_unit(army_id: int, unit_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    # Einheit löschen
    cursor.execute("""
        DELETE FROM army_units WHERE army_id=? AND unit_id=?
    """, (army_id, unit_id))
    conn.commit()

    # Validierung nach Entfernen
    if not validate_army(army_id):
        print("Essence Weaver fehlt – Entfernen wird rückgängig gemacht.")
        cursor.execute("""
            INSERT INTO army_units (army_id, unit_id, count)
            VALUES (?, ?, 1)
        """, (army_id, unit_id))
        conn.commit()

    conn.close()

def validate_army(army_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    
    # Gesamtpunkte prüfen
    cursor.execute("""
        SELECT SUM(u.cost * au.count)
        FROM army_units au
        JOIN units u ON au.unit_id = u.id
        WHERE au.army_id = ?
    """, (army_id,))
    total_points = cursor.fetchone()[0] or 0
    
    cursor.execute("SELECT max_points FROM armies WHERE id=?", (army_id,))
    max_points = cursor.fetchone()[0]
    
    if total_points > max_points:
        print("Punktebudget überschritten!")
        return False
    
    # Max 1 Commander prüfen
    cursor.execute("""
        SELECT COUNT(*) FROM army_units au
        JOIN units u ON au.unit_id = u.id
        WHERE au.army_id=? AND u.type='Commander'
    """, (army_id,))
    if cursor.fetchone()[0] > 1:
        print("Mehr als 1 Commander!")
        return False
    
    # Essence Weaver Pflicht
    cursor.execute("""
        SELECT COUNT(*) FROM army_units au
        JOIN units u ON au.unit_id = u.id
        WHERE au.army_id=? AND u.type='Essence Weaver'
    """, (army_id,))
    if cursor.fetchone()[0] < 1:
        print("Mindestens 1 Essence Weaver erforderlich!")
        return False
    
    # Max 4 normale Truppen prüfen
    cursor.execute("""
        SELECT u.name, au.count
        FROM army_units au
        JOIN units u ON au.unit_id = u.id
        WHERE au.army_id=? AND u.type!='Commander'
    """, (army_id,))
    for name, count in cursor.fetchall():
        if count > 4:
            print(f"{name} überschreitet Limit von 4!")
            return False
    
    conn.close()
    return True

def get_rulebook_path() -> str:
    return "rulebook/shroudfall_rulebook.pdf"

def search_rulebook(term: str) -> List[str]:
    results = []
    with open(get_rulebook_path(), "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if term.lower() in text.lower():
                results.append(f"Gefunden auf Seite {i+1}")
    return results

def get_update_info() -> List[Dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM updates ORDER BY date DESC")
    updates = cursor.fetchall()
    conn.close()
    return [{"version": u[1], "message": u[2], "date": u[3]} for u in updates]

def load_config():
    try:
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    except:
        return {"show_updates": True}

def save_config(cfg):
    with open(CONFIG_PATH, "w") as f:
        json.dump(cfg, f)

def should_show_updates():
    return load_config().get("show_updates", True)

def disable_updates():
    cfg = load_config()
    cfg["show_updates"] = False
    save_config(cfg)

def export_army(army_id: int, filepath: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT name, faction, max_points FROM armies WHERE id=?", (army_id,))
    army = cursor.fetchone()

    cursor.execute("""
        SELECT u.name, u.cost, au.count
        FROM army_units au
        JOIN units u ON au.unit_id = u.id
        WHERE au.army_id=?
    """, (army_id,))
    units = cursor.fetchall()

    conn.close()

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"Armee: {army[0]}\n")
        f.write(f"Fraktion: {army[1]}\n")
        f.write(f"Punktebudget: {army[2]}\n\n")
        f.write("Einheiten:\n")
        for name, cost, count in units:
            f.write(f"- {name} x{count} ({cost} Punkte)\n")

    print("Export erfolgreich!")

if __name__ == "__main__":
    print("Armeen:", load_armies())
    add_unit(3, 3, 1)
    remove_unit(3, 2)
    print("Validierung Armee 3:", validate_army(3))
    print("Regelbuch:", get_rulebook_path())
    print("Updates:", get_update_info())
