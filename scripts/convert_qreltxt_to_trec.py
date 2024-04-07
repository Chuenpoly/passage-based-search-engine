'''This script transform gov2_top50_doclist.txt to qrel format required in trev_eval'''

input_file = 'collection/WebAP/gov2_top50_doclist.txt'  # Path to the input file
output_file = 'collection/WebAP/qrels.gov2_top50_doclist.trec'  # Path to the output file

with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
    for line in f_in:
        parts = line.strip().split()
        query_id, doc_id, rank, _, _, _ = parts

        # Determine the relevance score based on the presence of 'R' or 'T'
        relevance_score = '1' if 'R' in parts or 'T' in parts else '0'

        f_out.write(f'{query_id} 0 {doc_id} {relevance_score}\n')