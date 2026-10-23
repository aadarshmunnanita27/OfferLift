from pathlib import Path
import argparse, sqlite3
import pandas as pd
p=argparse.ArgumentParser();p.add_argument('--data',required=True);a=p.parse_args()
d=pd.read_csv(a.data)
c=sqlite3.connect(':memory:');d.to_sql('customers',c,index=False)
for q in (Path(__file__).parent/'analysis.sql').read_text().split(';'):
    if q.strip(): print(pd.read_sql_query(q,c).to_string(index=False)+'\n')
