from flask import Flask, request, jsonify
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database", "shroudfall.db")

app = Flask(__name__)

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ---------------- ARMIES ----------------

@app.get("/armies")
def get_armies():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM armies")
    rows = cur.fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.get("/armies/<int:army_id>")
def get_army(army_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM armies WHERE id = ?", (army_id,))
    row = cur.fetchone()
    conn.close()

    if row is None:
        return jsonify({"error": "Army not found"}), 404

    return jsonify(dict(row))


# ---------------- UNITS IN ARMY ----------------

@app.get("/armies/<int:army_id>/units")
def get_army_units(army_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT au.id,
               au.count,
               u.id AS unit_id,
               u.name,
               u.points,
               u.type
        FROM army_units au
        JOIN units u ON u.id = au.unit_id
        WHERE au.army_id = ?
    """, (army_id,))
    rows = cur.fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.post("/armies/<int:army_id>/units/add")
def add_unit(army_id):
    data = request.json
    unit_id = data.get("unit_id")
    count = data.get("count", 1)

    conn = get_conn()
    cur = conn.cursor()

    # prüfen ob Armee existiert
    cur.execute("SELECT id FROM armies WHERE id = ?", (army_id,))
    if cur.fetchone() is None:
        conn.close()
        return jsonify({"error": "Army not found"}), 404

    # prüfen ob Unit existiert
    cur.execute("SELECT id FROM units WHERE id = ?", (unit_id,))
    if cur.fetchone() is None:
        conn.close()
        return jsonify({"error": "Unit not found"}), 404

    # prüfen ob Unit schon in Armee ist
    cur.execute("""
        SELECT id, count FROM army_units
        WHERE army_id = ? AND unit_id = ?
    """, (army_id, unit_id))
    row = cur.fetchone()

    if row:
        new_count = row["count"] + count
        cur.execute("UPDATE army_units SET count = ? WHERE id = ?", (new_count, row["id"]))
    else:
        cur.execute("""
            INSERT INTO army_units (army_id, unit_id, count)
            VALUES (?, ?, ?)
        """, (army_id, unit_id, count))

    conn.commit()
    conn.close()
    return jsonify({"status": "ok"})


@app.post("/armies/<int:army_id>/units/remove")
def remove_unit(army_id):
    data = request.json
    unit_id = data.get("unit_id")

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM army_units
        WHERE army_id = ? AND unit_id = ?
    """, (army_id, unit_id))
    conn.commit()
    conn.close()

    return jsonify({"status": "ok"})


# ---------------- UNITS (KARTEN) ----------------

@app.get("/units")
def get_units():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM units")
    rows = cur.fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.get("/units/<int:unit_id>")
def get_unit(unit_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM units WHERE id = ?", (unit_id,))
    row = cur.fetchone()
    conn.close()

    if row is None:
        return jsonify({"error": "Unit not found"}), 404

    return jsonify(dict(row))


# ---------------- START SERVER ----------------

if __name__ == "__main__":
    app.run(debug=True)
