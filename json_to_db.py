import json
from psycopg2.extras import execute_batch
from psycopg2 import connect
import os
import re

re_pattern = re.compile(u'[^\u0000]', re.UNICODE)


sql_text='''
INSERT INTO microsoft_academic_graph(id, paper) VALUES(%s, %s)
ON CONFLICT DO NOTHING;
'''

with open('password_file') as f:
    con = connect(f.read())

for file_name in os.listdir("."):
    if not file_name.endswith(".json"):
        continue    
    json_data = []
    with open(file_name) as f:
        previous = ""
        for line in f:
            try:
                filtered_string = line.replace("\\\\u0000","") 
                filtered_string = filtered_string.replace("\\u0000","") 
                row = json.loads(filtered_string)
                json_data.append(row)
            except Exception as err:
                print(previous)
                print("-------------------------")
                print(line)
                print("-------------------------")
                raise err
            else:
                previous = line
    print("\t\tGot",len(json_data),"rows to insert")
    with con.cursor() as cur:
        execute_batch(cur, sql_text, [(row["id"],json.dumps(row)) 
                                      for row in json_data], page_size=10000)
con.commit()
con.close()
