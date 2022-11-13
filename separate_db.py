import json
import argparse
import os 
from process_sql import Schema, get_sql, get_schema

def separate_table_database(file_path, dest_path, db_dir):
    with open(file_path) as f:
        olist = [l.strip().split('\t') for l in f.readlines() if len(l.strip()) > 0]

    nlist = []
    for o in olist:
        g_str = o[0]
        db = o[1]
        db = os.path.join(db_dir, db, db + ".sqlite")
        schema = Schema(get_schema(db))
        g_sql = get_sql(schema, g_str)
        new_db = extract_change_db(g_sql['from']['table_units'][0][1])
        o[1] = new_db
        nlist.append(o)
    
    with open(dest_path, 'w') as fww:
        fww.writelines('\t'.join(n) + '\n' for n in nlist)


def extract_change_db(table):
    table_db_mapping = {'__log1__': 'process_mining_1', '__log2__': 'process_mining_2', '__log3__' : 'process_mining_3','__log4__': 'process_mining_4',
        '__log5__': 'process_mining_5','__log6__': 'process_mining_6', '__log7__': 'process_mining_7', '__log8__': 'process_mining_8'}
    return table_db_mapping[table]
   

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_path", dest="file_path", type=str)
    parser.add_argument("--dest_path", dest="dest_path", type=str)
    parser.add_argument("--db_dir", dest="db_dir", type=str)

    args = parser.parse_args()

    file_path = args.file_path
    dest_path = args.dest_path
    db_dir = args.db_dir

    separate_table_database(file_path, dest_path, db_dir)

