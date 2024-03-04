import os
import re
import json

def convert_to_jsonl(file_path):
    output_directory = 'collection/processing/jsonl_file'
    os.makedirs(output_directory, exist_ok=True)
    output_file_path = os.path.join(output_directory, 'webap_discourse_docid_content.jsonl')

    with open(file_path, 'r', encoding='utf-8') as file:
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

    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write('\n'.join(jsonl_data))

file_path = 'collection/WebAP/gradedText/grade.trectext_patched'
convert_to_jsonl(file_path)