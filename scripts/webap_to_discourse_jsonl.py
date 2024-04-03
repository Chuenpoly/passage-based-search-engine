""" This script helps to transform the webap documents into discourse passages 
jsonl format that can be load and indexed by pyserini """

import os
import re
import json

def convert_to_jsonl(filepath):
    output_dir = 'collection\processing\jsonl_file'
    os.makedirs(output_dir, exist_ok=True)
    output_filepath = os.path.join(output_dir, 'webap_discourse_docid_content.jsonl')

    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()

    doc_blocks = re.findall(r'<DOC>(.*?)</DOC>', content, re.DOTALL)

    jsonl_data = []
    for i, doc_block in enumerate(doc_blocks, 1):
        docno = re.search(r'<DOCNO>(.*?)</DOCNO>', doc_block).group(1)
        sentences = re.findall(r'<SENTENCE>(.*?)</SENTENCE>', doc_block, re.DOTALL)

        for j, sentence in enumerate(sentences, 1):
            sentence_id = f"{docno}-{j}"
            json_data = {
                'id': sentence_id,
                'contents': sentence.strip()
            }
            jsonl_data.append(json.dumps(json_data))

    with open(output_filepath, 'w', encoding='utf-8') as output_file:
        output_file.write('\n'.join(jsonl_data))

filepath = 'collection\WebAP\gradedText\grade.trectext_patched'
convert_to_jsonl(filepath)