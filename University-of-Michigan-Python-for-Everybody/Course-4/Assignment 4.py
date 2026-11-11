import json
import sqlite3

# 1. Connect to the SQLite database
conn = sqlite3.connect('rosterdb.sqlite')
cur = conn.cursor()

# 2. Rebuild the required Many-to-Many relational structure
cur.executescript('''
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Member;
DROP TABLE IF EXISTS Course;

CREATE TABLE User (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name   TEXT UNIQUE
);

CREATE TABLE Course (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title  TEXT UNIQUE
);

CREATE TABLE Member (
    user_id     INTEGER,
    course_id   INTEGER,
    role        INTEGER,
    PRIMARY KEY (user_id, course_id)
)
''')

# 3. Read and parse your personalized JSON roster data
filename = 'roster_data.json'
try:
    with open(filename, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
except FileNotFoundError:
    print(f"Error: Could not find '{filename}'. Make sure it's in this same folder!")
    exit()

print("Processing database entries...")

# 4. Map names, courses, and roles into the tables
for entry in json_data:
    name = entry[0]
    title = entry[1]
    role = entry[2]

    # Insert or ignore duplicate users
    cur.execute('INSERT OR IGNORE INTO User (name) VALUES ( ? )', (name, ))
    cur.execute('SELECT id FROM User WHERE name = ? ', (name, ))
    user_id = cur.fetchone()[0]

    # Insert or ignore duplicate courses
    cur.execute('INSERT OR IGNORE INTO Course (title) VALUES ( ? )', (title, ))
    cur.execute('SELECT id FROM Course WHERE title = ? ', (title, ))
    course_id = cur.fetchone()[0]

    # Insert or replace relational membership entry mapping keys + roles
    cur.execute('''INSERT OR REPLACE INTO Member (user_id, course_id, role) 
        VALUES ( ?, ?, ? )''', (user_id, course_id, role))

# Commit updates to the database file
conn.commit()

# 5. Run verification sample query requested by the page
print("\n--- Verifying Row Formatting Output Sample ---")
verify_query = '''
SELECT User.name, Course.title, Member.role FROM 
User JOIN Member JOIN Course 
ON User.id = Member.user_id AND Member.course_id = Course.id
ORDER BY User.name DESC, Course.title DESC, Member.role DESC LIMIT 2;
'''
for row in cur.execute(verify_query):
    print(f"{row[0]}|{row[1]}|{row[2]}")

# 6. Execute the final code calculation string matching your data
code_query = '''
SELECT 'XYZZY' || hex(User.name || Course.title || Member.role) AS X FROM 
User JOIN Member JOIN Course 
ON User.id = Member.user_id AND Member.course_id = Course.id
ORDER BY X LIMIT 1;
'''
cur.execute(code_query)
assignment_code = cur.fetchone()[0]

print("\n================================================")
print(" YOUR TARGET ASSIGNMENT CODE TO COPY:")
print(f" {assignment_code}")
print("================================================")

cur.close()
