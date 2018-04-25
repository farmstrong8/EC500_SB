import sqlite3
import json


conn = sqlite3.connect("mydatabase.db") #creates a physical copy of the database

cursor = conn.cursor()

# create a table with a column for text
cursor.execute("""CREATE TABLE albums
                  (title text)
               """)


page = open('airports.json', 'r') #open the json file
parsed = json.loads(page.read()) #get each item in the json
for item in parsed:
    print(item) #print the item
    cursor.execute('insert into albums values (?)',(item['code'],)) #store the code in the database
