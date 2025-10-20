import sqlite3

class Database:
    def __init__(self, db_name="artify_studio.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS creations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                image_path TEXT NOT NULL,
                transformation_type TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def save_creation(self, image_path, transformation_type):
        self.cursor.execute("INSERT INTO creations (image_path, transformation_type) VALUES (?, ?)", (image_path, transformation_type))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_creations(self):
        self.cursor.execute("SELECT * FROM creations ORDER BY created_at DESC")
        return self.cursor.fetchall()

    def save_setting(self, key, value):
        self.cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, value))
        self.conn.commit()

    def get_setting(self, key):
        self.cursor.execute("SELECT value FROM settings WHERE key=?", (key,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def __del__(self):
        self.conn.close()
