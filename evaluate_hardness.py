from evaluation import Evaluator
from process_sql import Schema, get_sql
import json
import argparse

def get_schemas_from_json(fpath):
    with open(fpath) as f:
        data = json.load(f)
    db_names = [db['db_id'] for db in data]

    tables = {}
    schemas = {}
    for db in data:
        db_id = db['db_id']
        schema = {} #{'table': [col.lower, ..., ]} * -> __all__
        column_names_original = db['column_names_original']
        table_names_original = db['table_names_original']
        tables[db_id] = {'column_names_original': column_names_original, 'table_names_original': table_names_original}
        for i, tabn in enumerate(table_names_original):
            table = str(tabn.lower())
            cols = [str(col.lower()) for td, col in column_names_original if td == i]
            schema[table] = cols
        schemas[db_id] = schema

    return schemas, db_names, tables

def evaluate_hardness(file_path, table_file):
    with open(file_path) as f:
        glist = [l.strip().split('\t') for l in f.readlines() if len(l.strip()) > 0]

    levels = ['easy', 'medium', 'hard', 'extra', 'all']
    evaluator = Evaluator()
    scores = {}
    
    for level in levels:
        scores[level] = {'count': 0, 'partial': {}, 'exact': 0.}
        scores[level]['exec'] = 0
    
    glist.sort(key=lambda x: x[2])
    for g in glist:
        g_str, db, x = g
        db_name = db
        schemas, db_names, tables = get_schemas_from_json(table_file)
        schema = Schema(schemas[db_name])
        g_sql = get_sql(schema, g_str)
        hardness = evaluator.eval_hardness(g_sql)
        scores[hardness]['count'] += 1
        scores['all']['count'] += 1
        print(hardness + ';' + g_str + ';' + x)
    
    for l in levels:
        print(l + ': ' + str(scores[l]['count']))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--file_path', dest='file_path', type=str)
    parser.add_argument('--table_path', dest='table_path', type=str)
    args = parser.parse_args()

    file_path = args.file_path
    table_path = args.table_path
    
    evaluate_hardness(file_path, table_path)