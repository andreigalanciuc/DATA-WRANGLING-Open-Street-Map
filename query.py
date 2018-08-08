
# coding: utf-8

# In[ ]:


import sqlite3
import csv
from pprint import pprint


# In[ ]:


sqlite_file = 'datawrangle.db'    # name of the sqlite database file

# Connect to the database
conn = sqlite3.connect(sqlite_file)

# Get a cursor object
cur = conn.cursor()

cur.execute('''DROP TABLE IF EXISTS nodes_tags''')
conn.commit()

# Create the table, specifying the column names and data types:
cur.execute('''
    CREATE TABLE nodes_tags(id INTEGER, key TEXT, value TEXT,type TEXT)
''')
# commit the changes
conn.commit()

# Read in the csv file as a dictionary, format the
# data as a list of tuples:
with open('nodes_tags.csv','rb') as fin:
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(i['id'].decode('utf-8'), i['key'].decode('utf-8'),i['value'].decode('utf-8'), i['type'].decode('utf-8')) for i in dr]
    
# insert the formatted data
cur.executemany("INSERT INTO nodes_tags(id, key, value,type) VALUES (?, ?, ?, ?);", to_db)
# commit the changes
conn.commit()

cur.execute('SELECT * FROM nodes_tags')
all_rows = cur.fetchall()
print('1):')
pprint(all_rows)

conn.close()


# In[ ]:


# Connect to the database
conn = sqlite3.connect(sqlite_file)

# Get a cursor object
cur = conn.cursor()

cur.execute('''DROP TABLE IF EXISTS nodes''')
conn.commit()

# Create the table, specifying the column names and data types:
cur.execute('''
    CREATE TABLE nodes(id INTEGER, lat REAL, lon REAL, user TEXT, uid INTEGER, version INTEGER, changeset INTEGER, timestamp TEXT)
''')
# commit the changes
conn.commit()

# Read in the csv file as a dictionary, format the
# data as a list of tuples:
with open('nodes.csv','rb') as fin:
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(i['id'].decode("utf-8"), i['lat'].decode("utf-8"),i['lon'].decode('utf-8'), i['user'].decode('utf-8'), i['uid'].decode('utf-8'), i['version'].decode('utf-8'), i['changeset'].decode('utf-8'), i['timestamp'].decode('utf-8')) for i in dr]
    
# insert the formatted data
cur.executemany("INSERT INTO nodes(id, lat, lon, user, uid, version, changeset, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?);", to_db)
# commit the changes
conn.commit()

cur.execute('SELECT * FROM nodes')
all_rows = cur.fetchall()
print('1):')
pprint(all_rows)

conn.close()


# In[ ]:


sqlite_file = 'datawrangle.db'    # name of the sqlite database file

# Connect to the database
conn = sqlite3.connect(sqlite_file)

# Get a cursor object
cur = conn.cursor()

cur.execute('''DROP TABLE IF EXISTS ways_tags''')
conn.commit()

# Create the table, specifying the column names and data types:
cur.execute('''
    CREATE TABLE ways_tags(id INTEGER, key TEXT, value TEXT,type TEXT)
''')
# commit the changes
conn.commit()

# Read in the csv file as a dictionary, format the
# data as a list of tuples:
with open('ways_tags.csv','rb') as fin:
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(i['id'].decode("utf-8"), i['key'].decode('utf-8'),i['value'].decode('utf-8'), i['type'].decode('utf-8')) for i in dr]
    
# insert the formatted data
cur.executemany("INSERT INTO ways_tags(id, key, value,type) VALUES (?, ?, ?, ?);", to_db)
# commit the changes
conn.commit()

cur.execute('SELECT * FROM ways_tags')
all_rows = cur.fetchall()
print('1):')
pprint(all_rows)

conn.close()


# In[ ]:


# Connect to the database
conn = sqlite3.connect(sqlite_file)

# Get a cursor object
cur = conn.cursor()

cur.execute('''DROP TABLE IF EXISTS ways''')
conn.commit()

# Create the table, specifying the column names and data types:
cur.execute('''
    CREATE TABLE ways(id INTEGER, user TEXT, uid INTEGER, version INTEGER, changeset INTEGER, timestamp TEXT)
''')
# commit the changes
conn.commit()

# Read in the csv file as a dictionary, format the
# data as a list of tuples:
with open('ways.csv','rb') as fin:
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(i['id'].decode("utf-8"), i['user'].decode('utf-8'), i['uid'].decode('utf-8'), i['version'].decode('utf-8'), i['changeset'].decode('utf-8'), i['timestamp'].decode('utf-8')) for i in dr]
    
# insert the formatted data
cur.executemany("INSERT INTO ways(id, user, uid, version, changeset, timestamp) VALUES (?, ?, ?, ?, ?, ?);", to_db)
# commit the changes
conn.commit()

cur.execute('SELECT * FROM ways')
all_rows = cur.fetchall()
print('1):')
pprint(all_rows)

conn.close()


# In[ ]:


# Connect to the database
conn = sqlite3.connect(sqlite_file)

# Get a cursor object
cur = conn.cursor()

cur.execute('''DROP TABLE IF EXISTS ways_nodes''')
conn.commit()

# Create the table, specifying the column names and data types:
cur.execute('''
    CREATE TABLE ways_nodes(id INTEGER, node_id INTEGER, position INTEGER)
''')
# commit the changes
conn.commit()

# Read in the csv file as a dictionary, format the
# data as a list of tuples:
with open('ways_nodes.csv','rb') as fin:
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(i['id'].decode("utf-8"), i['node_id'].decode('utf-8'), i['position'].decode('utf-8')) for i in dr]
    
# insert the formatted data
cur.executemany("INSERT INTO ways_nodes(id, node_id, position) VALUES (?, ?, ?);", to_db)
# commit the changes
conn.commit()

cur.execute('SELECT * FROM ways_nodes')
all_rows = cur.fetchall()
print('1):')
pprint(all_rows)

conn.close()


# In[ ]:


def number_of_nodes():
    result = cur.execute('SELECT COUNT(*) FROM nodes')
    return result.fetchone()[0]

def number_of_ways():
    result = cur.execute('SELECT COUNT(*) FROM ways')
    return result.fetchone()[0]

def number_of_unique_users():
    result = cur.execute('SELECT COUNT(DISTINCT(e.uid))             FROM (SELECT uid FROM nodes UNION ALL SELECT uid FROM ways) e')
    return result.fetchone()[0]

def number_of_users_contributing_once():
    result = cur.execute('SELECT COUNT(*)             FROM                 (SELECT e.user, COUNT(*) as num                  FROM (SELECT user FROM nodes UNION ALL SELECT user FROM ways) e                  GROUP BY e.user                  HAVING num=1) u')
    return result.fetchone()[0]

if __name__ == '__main__':
    
    con = sqlite3.connect("datawrangle.db")
    cur = con.cursor()
    
    print "Number of nodes: " , number_of_nodes()
    print "Number of ways: " , number_of_ways()
    print "Number of unique users: " , number_of_unique_users()
    print "Number of users contributing once: " , number_of_users_contributing_once()


# In[ ]:


#10 top contributing users.

cur.execute("SELECT e.user, COUNT(*) as num            FROM (SELECT user FROM nodes UNION ALL SELECT user FROM ways) e            GROUP BY e.user            ORDER BY num DESC            LIMIT 10;")

print(cur.fetchall())


# In[ ]:


#10 top ammenities.
cur.execute("SELECT value, COUNT(*) as num             FROM ways_tags            WHERE key='amenity'            GROUP BY value            ORDER BY num DESC            LIMIT 10;")

print(cur.fetchall())


# In[ ]:


#10 top types of buildings.
cur.execute("SELECT value, COUNT(*) as num             FROM ways_tags            WHERE key='building'            GROUP BY value            ORDER BY num DESC            LIMIT 10;")

print(cur.fetchall())

