import sqlite3

conn = sqlite3.connect(':memory:')
cur = conn.cursor()

cur.execute('''
CREATE TABLE Ages ( 
  name VARCHAR(128), 
  age INTEGER
)
''')

cur.execute('DELETE FROM Ages')
cur.execute("INSERT INTO Ages (name, age) VALUES ('Forbes', 40)")
cur.execute("INSERT INTO Ages (name, age) VALUES ('Gurveer', 13)")
cur.execute("INSERT INTO Ages (name, age) VALUES ('Stella', 25)")
cur.execute("INSERT INTO Ages (name, age) VALUES ('Kassia', 23)")
conn.commit()

cur.execute('SELECT hex(name || age) AS X FROM Ages ORDER BY X')
first_row = cur.fetchone()
print(first_row[0])

conn.close()
