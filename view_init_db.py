import sqlite3

# Connect to your database
conn = sqlite3.connect("database.db")
db = conn.cursor()

# Check users table
db.execute("SELECT * FROM users")
rows = db.fetchall()
print("Users table:", rows)

# Check presets table
db.execute("SELECT * FROM presets")
rows = db.fetchall()
print("Presets table:", rows)

conn.close()