import sqlite3
import time
import ssl
import urllib.request

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Connect to database and create the messages table
conn = sqlite3.connect('content.sqlite')
cur = conn.cursor()

cur.execute('''
    CREATE TABLE IF NOT EXISTS Messages
    (id INTEGER PRIMARY KEY, email TEXT, sent_at TEXT, subject TEXT, body TEXT)
''')

# Check where we left off in the database
cur.execute('SELECT max(id) FROM Messages')
row = cur.fetchone()
if row[0] is not None:
    start = row[0] + 1
else:
    start = 1

# Updated to secure HTTPS URL pattern for Dr. Chuck's repository
baseurl = "https://mbox.dr-chuck.net/sakai.devel/"

print(f"Starting spider from message ID: {start}")

# Ask the user how many messages to download
str_count = input("How many messages to retrieve? ")
count = int(str_count) if str_count else 10

many = 0
while many < count:
    current_id = start + many
    
    # Properly format the exact API endpoint route (e.g., id/id+1)
    url = f"{baseurl}{current_id}/{current_id + 1}"
    print(f"Retrieving: {url}")
    
    try:
        document = urllib.request.urlopen(url, context=ctx)
        text = document.read().decode('utf-8', errors='ignore')
        if document.getcode() != 200:
            print("Error code:", document.getcode())
            break
    except Exception as e:
        print("Unable to retrieve text:", e)
        break

    # Look for headers and separate the email text
    lines = text.split('\n')
    email = "Unknown"
    subject = "No Subject"
    sent_at = "Unknown"
    
    for line in lines:
        if line.startswith('From: '):
            email = line.replace('From: ', '').strip()
        elif line.startswith('Subject: '):
            subject = line.replace('Subject: ', '').strip()
        elif line.startswith('Date: '):
            sent_at = line.replace('Date: ', '').strip()
            
    # Insert data safely into SQLite
    cur.execute('''INSERT INTO Messages (id, email, sent_at, subject, body) 
                   VALUES (?, ?, ?, ?, ?)''', (current_id, email, sent_at, subject, text))
    
    many += 1
    if many % 5 == 0:
        conn.commit()
        print("--> Committing 5 records to database...")
        time.sleep(1) # Be nice to the server

conn.commit()
cur.close()
print(f"\nSuccessfully loaded {many} messages into content.sqlite!")
