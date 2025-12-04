import sqlite3
from typing import List
from datetime import datetime

class PantryRepository:
    """
    Handles all direst interaction with the SQLite database.
    Follows the Repository Pattern.
    """

    def __init__(self, db_name: str = "pantry.db"):
        self.db_name = db_name
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_name)
    
    def _init_db(self) -> None:
        """Initializes the database schema if it does not exist."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ingredients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    added_at TIMESTAMP
                )
            """)
            conn.commit()

    def add_item(self, name: str) -> bool:
        """
        Adds an item to the pantry.
        Returns True if successful, False if duplicate.
        """
        clean_name = name.strip().lower()
        if not clean_name:
            return False
        try:
            with self._get_connection() as conn:
                cursor = conn.execute()
                cursor.execute(
                    "INSERT INTO ingredients (name, added_at) VALUES (?, ?)",
                    (clean_name, datetime.now())
                )
                conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        
    def remove_item(self, name: str) -> None:
        with self._get_connection() as conn:
            conn.execute("DELETE FROM ingredients WHERE name = ?", (name,))
            conn.commit()

    def get_all_items(self) -> List[str]:
        with self._get_connection() as conn:
            cursor = conn.execute("SELECT name FROM ingredients ORDER BY added_at DESC")
            return [row[0] for row in cursor.fetchall()]
        
    def clear_all(self) -> None:
        with self._get_connection() as conn:
            conn.execute("DELETE FROM ingredients")
            conn.commit()