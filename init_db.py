import sqlite3
conn=sqlite3.connect("db.db")
c=conn.cursor()
c.execute("CREATE TABLE users(id INTEGER PRIMARY KEY,username TEXT,password TEXT)")
c.execute("CREATE TABLE students(id INTEGER PRIMARY KEY,name TEXT,marks INTEGER)")
conn.commit()
conn.close()
print("DB Ready")
