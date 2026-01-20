
import sqlite3

conn = sqlite3.connect("database.db")
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, role TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS cars (id INTEGER PRIMARY KEY, name TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS rides (id INTEGER PRIMARY KEY, date TEXT, time TEXT, start TEXT, end_location TEXT, car_id INTEGER, driver_id INTEGER, status TEXT DEFAULT 'čeká', approved INTEGER DEFAULT 0)")
c.execute("CREATE TABLE IF NOT EXISTS ride_logs (id INTEGER PRIMARY KEY, ride_id INTEGER, user TEXT, change TEXT, timestamp TEXT)")

c.execute("INSERT OR IGNORE INTO users VALUES (1,'Novák','ridic')")
c.execute("INSERT OR IGNORE INTO users VALUES (2,'Dvořák','ridic')")
c.execute("INSERT OR IGNORE INTO users VALUES (3,'Dispečer','dispecer')")
c.execute("INSERT OR IGNORE INTO cars VALUES (1,'Auto1')")
c.execute("INSERT OR IGNORE INTO cars VALUES (2,'Auto2')")
c.execute("INSERT OR IGNORE INTO rides VALUES (1,'2026-01-20','08:00','Praha','Brno',1,1,'čeká',0)")
c.execute("INSERT OR IGNORE INTO rides VALUES (2,'2026-01-20','09:00','Brno','Ostrava',2,2,'čeká',0)")

conn.commit()
conn.close()
