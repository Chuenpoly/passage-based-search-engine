""" This script helps to transform the webap documents into jsonl format that can be load and indexed by pyserini """

import os
import re
import json

def convert_to_jsonl(filepath):
    output_dir = 'collection/processing/jsonl_file'
    os.makedirs(output_dir, exist_ok=True)
    output_filepath = os.path.join(output_dir, 'webap_docid_content.jsonl')

    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()

    doc_blocks = re.findall(r'<DOC>(.*?)</DOC>', content, re.DOTALL)

    jsonl_data = []
    for i, doc_block in enumerate(doc_blocks, 1):
        docno = re.search(r'<DOCNO>(.*?)</DOCNO>', doc_block).group(1)
        sentences = re.findall(r'<SENTENCE>(.*?)</SENTENCE>', doc_block, re.DOTALL)
        
        # Merging sentences into one passage
        passage = ' '.join(sentences)
        
        # Attaching "-1" to the ID, to ensure it is the same format as the passage-based method
        docno_with_suffix = f"{docno}-1"
        
        json_data = {
            'id': docno_with_suffix,
            'contents': passage.strip()
        }
        jsonl_data.append(json.dumps(json_data))

    with open(output_filepath, 'w', encoding='utf-8') as output_file:
        output_file.write('\n'.join(jsonl_data))

filepath = 'collection/WebAP/gradedText/grade.trectext_patched'
convert_to_jsonl(filepath)
