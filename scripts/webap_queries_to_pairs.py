""" This script helps to transform the webap queries into text file with tab-delimited (query id, query) pairs that 
can be load and iterated by pyserini """

import json

input_file = 'collection\WebAP\gradedText\gov2.query.json'
output_file = 'collection\processing\queries\queries.txt'

with open(input_file, 'r', encoding='utf-8') as inputFile:
    content = json.load(inputFile)

# remove the outter queries key
queries = content['queries']

with open(output_file, 'w', encoding='utf-8') as outputFile:
    for query in queries:
        query_id = query['number']
        query_text = query['text']
        outputFile.write(f"{query_id}\t{query_text}\n")