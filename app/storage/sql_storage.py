import sqlite3
from .storage import StorageBase

class SQLStorage(StorageBase):
    def __init__(self, db_name: str):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS products
                               (product_title TEXT PRIMARY KEY, product_price REAL, image_url TEXT)''')

    def save(self, data: list):
        for item in data:
            self.cursor.execute('''INSERT OR REPLACE INTO products (product_title, product_price, image_url)
                                   VALUES (?, ?, ?)''', 
                                   (item['product_title'], item['product_price'], item['image_url']))
        self.conn.commit()

    def load(self) -> list:
        self.cursor.execute('SELECT * FROM products')
        rows = self.cursor.fetchall()
        return [{'product_title': row[0], 'product_price': row[1], 'image_url': row[2]} for row in rows]

    def update_data(self, new_data: list) -> int:
        current_data = self.load()
        updated_data = []
        for new_item in new_data:
            for current_item in current_data:
                if current_item['product_title'] == new_item['product_title']:
                    if current_item['product_price'] != new_item['product_price']:
                        updated_data.append(new_item)
                    break
            else:
                updated_data.append(new_item)
        self.save(updated_data)
        return len(updated_data)
