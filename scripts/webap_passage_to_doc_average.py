"""This script transfer batch retrieval passages score to document scores using average operator."""

from collections import defaultdict

input_file = 'collection/processing/batch_retrieval_results/run.webap.bm25tuned.trec'
output_file = 'collection/processing/document_results/run.webap.bm25tuned.average.trec'

document_scores = defaultdict(list)

with open(input_file, 'r') as file:
    for line in file:
        parts = line.split()
        qid = parts[0]
        passage_id = parts[2]
        rank = int(parts[3])
        score = float(parts[4])

        document_id = '-'.join(passage_id.split('-')[:-2])
        document_scores[qid].append((document_id, score))

document_score_lines = []
for qid in sorted(document_scores.keys()):
    doc_scores = document_scores[qid]
    document_score_dict = defaultdict(list)
    
    # Calculate average passage score for each document
    for document_id, score in doc_scores:
        document_score_dict[document_id].append(score)
    
    # Calculate average document score
    sorted_docs = sorted(document_score_dict.items(), key=lambda x: sum(x[1]) / len(x[1]), reverse=True)
    for new_rank, (document_id, scores) in enumerate(sorted_docs, start=1):
        average_score = sum(scores) / len(scores)
        document_score_lines.append(f'{qid} Q0 {document_id} {new_rank} {average_score:.6f} Anserini\n')

with open(output_file, 'w') as file:
    file.writelines(document_score_lines)