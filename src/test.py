import os
DB_PATH = os.path.abspath("database/database.db")
print(f"📂 Database Path: {DB_PATH}")
print(f"📝 File exists? {os.path.exists(DB_PATH)}")
