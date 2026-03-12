import pandas as pd
import sqlite3

df = pd.read_csv("animedataset.csv")

connectSQLite = sqlite3.connect("anime.db")

df.to_sql("anime", connectSQLite, if_exists="replace", index=False)

cursor = connectSQLite.cursor()
cursor.execute("SELECT COUNT(*) FROM anime")
count = cursor.fetchone()
print(f"Database created. Loaded {count[0]} rows")

cursor.execute("SELECT * FROM anime LIMIT 3")
rows = cursor.fetchall()
print("\nFirst 3 rows:")
for row in rows:
    print(row)

connectSQLite.close()
print("\nDatabase setup done")