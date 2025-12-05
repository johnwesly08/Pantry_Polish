# src/database.py
import sqlite3
from typing import List, Dict
from src.seeds import RECIPE_SEEDS

class PantryRepository:
    def __init__(self, db_name="pantry.db"):
        self.db_name = db_name
        self._init_db()

    def _get_conn(self):
        return sqlite3.connect(self.db_name)

    def _init_db(self):
        """Creates tables and seeds data from seeds.py if DB is empty."""
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS inventory (item TEXT PRIMARY KEY)")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS recipes (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    image TEXT,
                    ingredients TEXT,
                    time TEXT,
                    cal INTEGER
                )
            """)
            
            cursor.execute("SELECT count(*) FROM recipes")
            if cursor.fetchone()[0] == 0:
                print("--- SEEDING DATABASE FROM SEEDS.PY ---")
                for r in RECIPE_SEEDS:
                    cursor.execute("""
                        INSERT INTO recipes (name, image, ingredients, time, cal)
                        VALUES (?, ?, ?, ?, ?)
                    """, (r['name'], r['image'], r['ingredients'], r['time'], r['cal']))
            conn.commit()

    def add_item(self, item: str):
        clean = item.strip().lower()
        if not clean: return False
        try:
            with self._get_conn() as conn:
                conn.execute("INSERT INTO inventory (item) VALUES (?)", (clean,))
            return True
        except sqlite3.IntegrityError:
            return False

    def remove_item(self, item: str):
        with self._get_conn() as conn:
            conn.execute("DELETE FROM inventory WHERE item = ?", (item,))

    def get_inventory(self) -> List[str]:
        with self._get_conn() as conn:
            cursor = conn.execute("SELECT item FROM inventory")
            return [row[0] for row in cursor.fetchall()]

    def get_all_recipes(self) -> List[Dict]:
        with self._get_conn() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM recipes")
            return [dict(row) for row in cursor.fetchall()]