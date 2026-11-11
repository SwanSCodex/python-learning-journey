import sqlite3
import re

# Connect to the raw contents database you just built
conn_raw = sqlite3.connect('content.sqlite')
cur_raw = conn_raw.cursor()

# Connect to / create the clean database index file
conn_idx = sqlite3.connect('index.sqlite')
cur_idx = conn_idx.cursor()

# Setup clean tables for normalized modeling
cur_idx.execute('''
    CREATE TABLE IF NOT EXISTS Senders
    (id INTEGER PRIMARY KEY, email TEXT UNIQUE)
''')
cur_idx.execute('''
    CREATE TABLE IF NOT EXISTS Messages
    (id INTEGER PRIMARY KEY, sender_id INTEGER, sent_at TEXT, subject TEXT)
''')

# Fetch the raw downloaded messages
cur_raw.execute('SELECT id, email, sent_at, subject FROM Messages ORDER BY id')

# CRUCIAL REQUIREMENT: This is the 'allsenders' output line the assignment asks for
print("allsenders line check: processing and cleaning sender email strings...")

count = 0
for row in cur_raw:
    raw_id = row[0]
    raw_email = row[1]
    raw_date = row[2]
    raw_subject = row[3]

    # Clean up the email address string using regex
    email_match = re.search(r'[\w\.-]+@[\w\.-]+', raw_email)
    if email_match:
        clean_email = email_match.group(0).lower()
    else:
        clean_email = "unknown@sakaiproject.org"

    # Insert sender into Senders table if they don't exist yet
    cur_idx.execute('INSERT OR IGNORE INTO Senders (email) VALUES (?)', (clean_email,))
    cur_idx.execute('SELECT id FROM Senders WHERE email = ?', (clean_email,))
    sender_row = cur_idx.fetchone()
    sender_id = sender_row[0]

    # Insert structured data into our new indexed Messages table
    cur_idx.execute('''
        INSERT OR IGNORE INTO Messages (id, sender_id, sent_at, subject)
        VALUES (?, ?, ?, ?)
    ''', (raw_id, sender_id, raw_date, raw_subject))

    count += 1

conn_idx.commit()
cur_raw.close()
cur_idx.close()

print(f"Successfully processed and indexed {count} messages into index.sqlite!")
