"""This script transfer batch retrieval passages score to document scores using sum operator."""

from collections import defaultdict

input_file = 'collection/processing/batch_retrieval_results/run.webap.bm25tuned.trec'
output_file = 'collection/processing/document_results/run.webap.bm25tuned.sum_topk.trec'

document_scores = defaultdict(lambda: defaultdict(list))
topk = 5  # Specify the value of 'k' for selecting the top k passages

with open(input_file, 'r') as file:
    for line in file:
        parts = line.split()
        qid = parts[0]
        passage_id = parts[2]
        rank = int(parts[3])
        score = float(parts[4])

        document_id = '-'.join(passage_id.split('-')[:-2])
        document_scores[qid][document_id].append(score)

document_score_lines = []
for qid in sorted(document_scores.keys()):
    doc_scores = document_scores[qid]
    document_score_list = []
    for document_id, passage_scores in doc_scores.items():
        # Select the top k passage scores
        topk_scores = sorted(passage_scores, reverse=True)[:topk]
        
        # Calculate the sum of the top k passage scores
        document_score = sum(topk_scores)
        
        document_score_list.append((document_id, document_score))
    
    # Sort documents based on the document score
    sorted_docs = sorted(document_score_list, key=lambda x: x[1], reverse=True)
    
    # Assign ranks based on the sorted order
    for new_rank, (document_id, score) in enumerate(sorted_docs, start=1):
        document_score_lines.append(f'{qid} Q0 {document_id} {new_rank} {score:.6f} Anserini\n')

with open(output_file, 'w') as file:
    file.writelines(document_score_lines)