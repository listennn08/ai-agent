import sqlite3

from langchain_core.output_parsers import json


class DrinkRepository:
    def __init__(self, name = "drinks.db"):
        self.db_path = f"app/storage/db/{name}"
        self._initialize_db()

  
    def _initialize_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS drinks (
        id INTEGER PRIMARY KEY,  -- FAISS 索引 ID
        sku TEXT,
        name TEXT,
        drink_category TEXT,
        json_data TEXT
        )
        """)
        conn.commit()
        conn.close()

    
    def insert_drinks(self, drinks, start_index):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        for i, drink in enumerate(drinks):
            cursor.execute("""
            INSERT INTO drinks (id, sku, name, drink_category, json_data)
            VALUES (?, ?, ?, ?, ?)
            """, (start_index + i, drink.sku, drink.name, drink.drink_category, drink.json_data))
        
        conn.commit()
        conn.close()

    
    def get_drink_by_id(self, drink_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT sku, name, drink_category, json_data FROM drinks WHERE id=?", (drink_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return {
                "sku": row[0],
                "name": row[1],
                "category": row[2],
                "ingredients": json.loads(row[3])["ingredients"]
            }
        
        return None

