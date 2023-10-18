'''
Create database files and database tables
'''
import sqlite3
conn = sqlite3.Connection('dataBaseOfDistance.db')
print("The first step worked!")

conn.execute('''
    CREATE TABLE distance
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    date CHAR(50),
    distance_data Float,
    status CHAR(50),
    waterLevel Float
    );
''')
print("The sencod step worked!")
conn.close()