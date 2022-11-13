import argparse

def add_db_info(file_reference, file_target, output_file):
    with open(file_reference) as f:
        reference_list = [l.strip().split('\t') for l in f.readlines() if len(l.strip()) > 0]

    with open(file_target) as f:
        reference_target = [l.strip().split('\t') for l in f.readlines() if len(l.strip()) > 0]

    with open(output_file, 'w') as fw:
        for rf, t in zip(reference_list, reference_target):
            fw.write(t[0] + "\t" + rf[1] + "\n")
   
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_reference", dest="file_reference", type=str)
    parser.add_argument("--file_target", dest="file_target", type=str)
    parser.add_argument("--output_file", dest="output_file", type=str)
    
    args = parser.parse_args()

    file_reference = args.file_reference
    file_target = args.file_target
    output_file = args.output_file
    
    add_db_info(file_reference, file_target, output_file)
