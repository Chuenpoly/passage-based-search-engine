#activate the venv
source env/bin/activate

#run the program locally
python app.py

#Do we need to upload virtual env on github too?
https://stackoverflow.com/questions/51863155/do-we-need-to-upload-virtual-env-on-github-too

#convert the webap document into somthing pyserini indexer can read
python webap_to_discourse_jsonl.py

#create inverted index (takes ~1 min for 2 threads)
#take the jsonl input file from collection/processing 
#put the index file into collection/processing/indexes
python3 -m pyserini.index.lucene --collection JsonCollection --input collection/processing/jsonl_file --index collection/processing/indexes --generator DefaultLuceneDocumentGenerator --threads 2 --storePositions --storeDocvectors –storeRaw