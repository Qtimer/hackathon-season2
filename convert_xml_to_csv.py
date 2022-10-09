import sqlite3
import pandas as pd
import csv
df = pd.read_xml('data-devclub-1.xml')
header = df.keys()
with open('data-devclub.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    for current_row in range(len(df)):
        data = [df[column_name][current_row] for column_name in header]
        writer.writerow(data)
