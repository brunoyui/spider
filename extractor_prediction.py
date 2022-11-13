from __future__ import print_function
import json

import argparse

def read_generate_predicted(file, file_dev, output_file, output_file_g):
    with open(file) as f:
        data = json.load(f)
    
    with open(file_dev) as f:
        data_dev = json.load(f)

    predicted_sql = []
    gold_sql = []
    eval_by_item = data["per_item"]
    for e in eval_by_item:
        if (e["predicted"] is not None):
            predicted_sql.append(e["predicted"])
            gold_sql.append(e["gold"])
        else:
            predicted_sql.append('null')
            gold_sql.append(e["gold"])


    
    print(len(predicted_sql))
    with open(output_file, 'w') as fw:
        for index, v in enumerate(predicted_sql):
            fw.write(v + "\t" + data_dev[index]['db_id'] + "\n")
    
    print(len(gold_sql))
    with open(output_file_g, 'w') as fww:
        for index, g in enumerate(gold_sql):
            fww.write(g + "\t" + data_dev[index]['db_id'] + "\n")
    
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', dest='file', type=str)
    parser.add_argument('--file_dev', dest='file_dev', type=str)
    parser.add_argument('--output_file_predicted', dest='output_file_predicted', type=str)
    parser.add_argument('--output_file_gold', dest='output_file_gold', type=str)
    
    args = parser.parse_args()

    file = args.file
    file_dev = args.file_dev
    output_file_predicted = args.output_file_predicted
    output_file_gold = args.output_file_gold

    read_generate_predicted(file, file_dev, output_file_predicted, output_file_gold)    
    