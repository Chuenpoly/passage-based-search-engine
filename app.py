from flask import Flask, render_template, request
from pyserini.search.lucene import LuceneSearcher
import time

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form.get('query')

        start = time.time()

        # Process the query here in backend
        # use the inverted index and user query to retrieve the documents
        searcher = LuceneSearcher('collection/processing/indexes')
        hits = searcher.search(query, k=searcher.num_docs)

        # Save the passage search results to a file
        with open('collection/processing/passage_results/passage_scores.txt', 'w') as file:
            for i in range(len(hits)):
                file.write(f'{i+1:2} {hits[i].docid:4} {hits[i].score:.8f}\n')

        # Read the passage search results file
        with open('collection/processing/passage_results/passage_scores.txt', 'r') as file:
            lines = file.readlines()

        # Dictionary to store document scores and corresponding passage IDs
        document_scores = {}
        document_passage_ids = {}

        # Loop through the lines and combine passage scores
        for line in lines:
            rank, doc_id, score = line.strip().split(' ')
            document_id = '-'.join(doc_id.split('-')[:-1])  # Extract the document ID
            passage_id = doc_id.split('-')[-1]  # Extract the passage ID
            passage_score = float(score)

            if document_id not in document_scores:
                document_scores[document_id] = passage_score
                document_passage_ids[document_id] = passage_id
            else:
                if passage_score > document_scores[document_id]:
                    document_scores[document_id] = passage_score
                    document_passage_ids[document_id] = passage_id

        # Sort the document scores in descending order
        sorted_scores = sorted(document_scores.items(), key=lambda x: x[1], reverse=True)

        # Write the combined document scores to a file
        with open('collection/processing/document_results/document_scores.txt', 'w') as output_file:
            for i, (document_id, score) in enumerate(sorted_scores):
                passage_id = document_passage_ids[document_id]
                output_file.write(f'{i+1} {document_id} {score:.5f} {passage_id}\n')
        
        # Read the document scores file
        with open('collection/processing/document_results/document_scores.txt', 'r') as file:
            results = file.readlines()

        # End of processing
        end = time.time()
        runtime = end - start
        num_retrieved = len(results)
        
        return render_template('index.html', query=query, results=results, num_retrieved=num_retrieved, runtime=runtime)
    else:
        return render_template('index.html')

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)