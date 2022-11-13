from __future__ import print_function
import json

import argparse

from process_sql import tokenize, get_sql

class Schema:
    """
    Simple schema which maps table&column to a unique identifier
    """
    def __init__(self, schema, table):
        self._schema = schema
        self._table = table
        self._idMap = self._map(self._schema, self._table)

    @property
    def schema(self):
        return self._schema

    @property
    def idMap(self):
        return self._idMap

    def _map(self, schema, table):
        column_names_original = table['column_names_original']
        table_names_original = table['table_names_original']
        #print 'column_names_original: ', column_names_original
        #print 'table_names_original: ', table_names_original
        for i, (tab_id, col) in enumerate(column_names_original):
            if tab_id == -1:
                idMap = {'*': i}
            else:
                key = table_names_original[tab_id].lower()
                val = col.lower()
                idMap[key + "." + val] = i

        for i, tab in enumerate(table_names_original):
            key = tab.lower()
            idMap[key] = i

        return idMap

def build_foreign_key_map(entry):
    cols_orig = entry["column_names_original"]
    tables_orig = entry["table_names_original"]

    # rebuild cols corresponding to idmap in Schema
    cols = []
    for col_orig in cols_orig:
        if col_orig[0] >= 0:
            t = tables_orig[col_orig[0]]
            c = col_orig[1]
            cols.append("__" + t.lower() + "." + c.lower() + "__")
        else:
            cols.append("__all__")

    def keyset_in_list(k1, k2, k_list):
        for k_set in k_list:
            if k1 in k_set or k2 in k_set:
                return k_set
        new_k_set = set()
        k_list.append(new_k_set)
        return new_k_set

    foreign_key_list = []
    foreign_keys = entry["foreign_keys"]
    for fkey in foreign_keys:
        key1, key2 = fkey
        key_set = keyset_in_list(key1, key2, foreign_key_list)
        key_set.add(key1)
        key_set.add(key2)

    foreign_key_map = {}
    for key_set in foreign_key_list:
        sorted_list = sorted(list(key_set))
        midx = sorted_list[0]
        for idx in sorted_list:
            foreign_key_map[cols[idx]] = cols[midx]

    return foreign_key_map


def build_foreign_key_map_from_json(table):
    with open(table) as f:
        data = json.load(f)
    tables = {}
    for entry in data:
        tables[entry['db_id']] = build_foreign_key_map(entry)
    return tables

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

def generate_json(file, table, output_file, kmaps):
    with open(file) as f:
        glist = [l.strip().split('\t') for l in f.readlines() if len(l.strip()) > 0]
    
    json_data = []
    print(glist)
    #glist.sort(key=lambda x: x[2])
    schemas, db_names, tables = get_schemas_from_json(table)
    for g in glist:
        print(g)
        sql_str, db_name, id, question = g
        print(id)
        schema = Schema(schemas[db_name], tables[db_name])
        data = get_object_info(sql_str, db_name, question, schema)
        json_data.append(data)

    with open(output_file, 'wt') as out:
        json.dump(json_data, out, sort_keys=True, indent=4, separators=(',', ': '))

def get_object_info(sql_str, db_name, question, schema):
    data = {}
    data["db_id"] = db_name
    data["query"] = sql_str
    data["query_toks"] = tokenize(sql_str)
    data["question"] = question
    data["question_toks"] = tokenize(question)
    sql_transform = get_sql(schema, sql_str)
    data["sql"] = sql_transform
    return data

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--file_path', dest='file_path', type=str)
    parser.add_argument('--table_path', dest='table_path', type=str)
    parser.add_argument('--output_file', dest='output_file', type=str)
    
    args = parser.parse_args()

    file_path = args.file_path
    table_path = args.table_path
    output_file = args.output_file
 
    kmaps = build_foreign_key_map_from_json(table_path)
    print(kmaps)
    
    generate_json(file_path, table_path, output_file, kmaps)