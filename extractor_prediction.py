from __future__ import print_function
import json

import argparse

def read_generate_predicted(file, output_file, output_file_g):
    with open(file) as f:
        data = json.load(f)
    
    predicted_sql = []
    gold_sql = []
    eval_by_item = data["per_item"]
    for e in eval_by_item:
        if (e["predicted"] is not None):
            predicted_sql.append(e["predicted"])
            gold_sql.append(e["gold"])
    
    print(len(predicted_sql))
    with open(output_file, 'w') as fw:
        for v in predicted_sql:
            print(v)
            fw.write(v + "\t" + "process_mining" + "\n")
    
    print(len(gold_sql))
    with open(output_file_g, 'w') as fww:
        for g in gold_sql:
            fww.write(g + "\t" + "process_mining" + "\n")
    
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', dest='file', type=str)
    parser.add_argument('--output_file_predicted', dest='output_file_predicted', type=str)
    parser.add_argument('--output_file_gold', dest='output_file_gold', type=str)
    

    args = parser.parse_args()

    file = args.file
    output_file_predicted = args.output_file_predicted
    output_file_gold = args.output_file_gold

    read_generate_predicted(file, output_file_predicted, output_file_gold)    
    