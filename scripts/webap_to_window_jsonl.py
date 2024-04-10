""" This script helps to transform the webap documents into specified window size passages 
jsonl format that can be load and indexed by pyserini """

import os
import re
import json

def convert_to_jsonl(file_path, window_size):
    output_dir = 'collection/processing/jsonl_file'
    os.makedirs(output_dir, exist_ok=True)
    output_filepath = os.path.join(output_dir, 'webap_docid_content.jsonl')

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    doc_blocks = re.findall(r'<DOC>(.*?)</DOC>', content, re.DOTALL)

    jsonl_data = []
    for i, doc_block in enumerate(doc_blocks, 1):
        docno = re.search(r'<DOCNO>(.*?)</DOCNO>', doc_block).group(1)
        sentences = re.findall(r'<SENTENCE>(.*?)</SENTENCE>', doc_block, re.DOTALL)

        combined_sentence = ' '.join(sentences)
        words = combined_sentence.strip().split()
        num_words = len(words)

        passage_id = 1
        for k in range(0, num_words, window_size):
            start_idx = k
            end_idx = min(k + window_size, num_words)
            window_words = words[start_idx:end_idx]
            window_sentence = ' '.join(window_words)

            json_data = {
                'id': f"{docno}-{passage_id}",
                'contents': window_sentence
            }
            jsonl_data.append(json.dumps(json_data))

            passage_id += 1

    with open(output_filepath, 'w', encoding='utf-8') as output_file:
        output_file.write('\n'.join(jsonl_data))

file_path = 'collection/WebAP/gradedText/grade.trectext_patched'
window_size = 40  # Specify the desired window size here
convert_to_jsonl(file_path, window_size)