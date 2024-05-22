

import sqlite3
con = sqlite3.connect("tutorial.db")    # IMPLICITLY CREATES DB IF DOESN'T ALREADY EXIST.

# In order to execute SQL statements and fetch results from SQL queries, we will need to use a database cursor. Call con.cursor() to create the Cursor:

cur = con.cursor()

# create a database table called "movie" with columns for title, release year, and review score. Thanks to the flexible typing feature of SQLite, specifying the data types is optional

try:
    cur.execute("CREATE TABLE movie(title, year, score)") 
except:
    pass 
    
# verify that the new table has been created by querying the "sqlite_master" table built-in to SQLite, which should now contain an entry for the movie table definition

res = cur.execute("SELECT name FROM sqlite_master")

print(res.fetchone())	# fetch the resulting row.

# look for a table that doesn't exist.
res = cur.execute("SELECT name FROM sqlite_master WHERE name='spam'")
print(res.fetchone())

# add 2 rows of data to the table
# INSERT statement implicitly opens a transaction, which needs to be committed before changes are saved in the database
cur.execute("""
    INSERT INTO movie VALUES
        ('Monty Python and the Holy Grail', 1975, 8.2),
        ('And Now for Something Completely Different', 1971, 7.5)
""")
con.commit() 

# verify that the data was inserted correctly by executing a SELECT query. 
res = cur.execute("SELECT score FROM movie")
print(res.fetchall() )       # fetch all rows.



