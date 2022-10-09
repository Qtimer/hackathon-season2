import sqlite3
from numpy import empty
import pandas as pd
import os
import csv
from datetime import datetime, timedelta

to_import_file_name = 'data-devclub.csv'
initial_xml_file_name = 'data-devclub-1.xml'  # for the schema
try:
    ### read header to get intial schema
    df = pd.read_xml(initial_xml_file_name)
    header = df.keys()
    column_names = ', '.join(header)

    ### initial sqlite table
    TABLE_NAME = 'EMPLOYEE'
    con = sqlite3.connect("employee.db")
    cur = con.cursor()
    cur.execute(f'''CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        EMPID integer PRIMARY KEY, 
        PASSPORT text, 
        FIRSTNAME text, 
        LASTNAME text, 
        GENDER integer, 
        BIRTHDAY text, 
        NATIONALITY text, 
        HIRED text, 
        DEPT text, 
        POSITION text, 
        STATUS integer, 
        REGION text
        );''')
    con.commit()
    
    #### import CSV file ######
    with open(to_import_file_name) as file:
        csvreader = csv.reader(file)
        header = []
        header = next(csvreader)
        rows = []
        empty_values = ','.join(['?' for i in header])
        for row in csvreader:
            sql = f''' INSERT INTO {TABLE_NAME}(EMPID, PASSPORT, FIRSTNAME, LASTNAME, GENDER, BIRTHDAY, NATIONALITY, HIRED, DEPT, POSITION, STATUS, REGION)
                    VALUES({empty_values}) '''
            # condition to not create
            # 1. dup data
            # 2. empid=passport_no
            # 3. left the comp (status=2)
            # 4. DEPT = airhostress, pilot, steward
            # 5. work exp. more than 3 years
            condition_1 = False  # โจทย์ไม่เคลียว่า dup คึอแค่ไหน
            condition_2 = row[0] == row[1]
            condition_3 = f'{row[10]}'.isnumeric() and int(row[10]) == 3
            condition_4 = row[8] not in ['Airhostess', 'Pilot', 'Steward']
            condition_5 = (datetime.now() - datetime.strptime(row[7], '%d-%M-%Y')) < timedelta(days=365*3)
            if condition_1 or condition_2 or condition_3 or condition_4 or condition_5:
                continue
            cur.execute(sql, row)
    con.commit()
    cur.execute(f'select count(*) from {TABLE_NAME}')
    print(cur.fetchone())
    
    ### create view
    cur.execute('''CREATE VIEW V_NATION
                AS SELECT EMPID, NATIONALITY
                FROM EMPLOYEE
                ''')
    cur.execute('''CREATE VIEW V_DEPT
                AS SELECT EMPID, DEPT
                FROM EMPLOYEE
                ''')
    cur.execute('''CREATE VIEW V_REGION
                AS SELECT EMPID, REGION
                FROM EMPLOYEE
                ''')
    # cur.execute('select count(*), REGION from v_REGION group by REGION')
    # print(cur.fetchall())
    con.close()
except Exception as e:
    import traceback
    traceback.print_exc()
finally:
    con.close()
#     os.system('rm -f employee.db')