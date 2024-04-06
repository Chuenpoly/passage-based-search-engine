"""This script transfer batch retrieval passages score to document scores using max operator."""

from collections import defaultdict

input_file = 'collection/processing/batch_retrieval_results/run.webap.bm25tuned.trec'
output_file = 'collection/processing/document_results/eval_doc_score_max.trec'

document_scores = defaultdict(dict)

with open(input_file, 'r') as file:
    for line in file:
        parts = line.split()
        qid = parts[0]
        passage_id = parts[2]
        rank = int(parts[3])
        score = float(parts[4])

        document_id = '-'.join(passage_id.split('-')[:-2])
        if document_id not in document_scores[qid]:
            document_scores[qid][document_id] = (score, rank)
        else:
            prev_score, prev_rank = document_scores[qid][document_id]
            if score > prev_score or (score == prev_score and rank < prev_rank):
                document_scores[qid][document_id] = (score, rank)

document_score_lines = []
for qid in sorted(document_scores.keys()):
    doc_scores = document_scores[qid]
    sorted_docs = sorted(doc_scores.items(), key=lambda x: x[1][0], reverse=True)
    for new_rank, (document_id, (score, _)) in enumerate(sorted_docs, start=1):
        document_score_lines.append(f'{qid} Q0 {document_id} {new_rank} {score:.6f} Anserini\n')

with open(output_file, 'w') as file:
    file.writelines(document_score_lines)