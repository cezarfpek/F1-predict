import pandas as pd
import glob
import sqlite3

csv_files = glob.glob('data/*.csv')

conn = sqlite3.connect('data.db')


for file in csv_files:
    df = pd.read_csv(file)

    table_name = file.split('/')[-1].split('.')[0]
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.commit()
    
conn.close()