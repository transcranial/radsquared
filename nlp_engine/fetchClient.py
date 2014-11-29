import xmlrpc.client
import sys

try:
    
    port = sys.argv[1]
    s = xmlrpc.client.ServerProxy('http://localhost:' + port)
    sys.stdout.write(s.fetchRelevant(sys.argv[2], int(sys.argv[3])))

except:
    
    sys.stderr.write('unable to connect to XML-RPC server')

    from helperFunctions import pickle_zloads, pickle_zdumps
    import numpy
    import json
    import os

    from pymongo import MongoClient
    import gridfs
    db_uri = os.getenv('MONGOLAB_URI', 'mongodb://localhost:27017')
    client = MongoClient(db_uri)
    if 'localhost' in db_uri:    
        db = client['radsquared-dev']
    else:
        db = client['heroku_app24877560']
    fs = gridfs.GridFS(db)

    # loads snippet ids
    pklcompfile = fs.get_last_version(filename="python-data/snippetCollection_id.pkl").read()
    snippetCollection_id = pickle_zloads(pklcompfile)
    # loads vector array trained on corpus
    pklcompfile = fs.get_last_version(filename="python-data/trainedVectorArray.pkl").read()
    trainedVectorArray = pickle_zloads(pklcompfile)

    # sets up vectorizer
    from nltk.stem.snowball import SnowballStemmer
    import re
    from sklearn.feature_extraction.text import HashingVectorizer
    def stemTokenize(doc):
        stemmer = SnowballStemmer('english')
        return [stemmer.stem(word) for word in re.findall(r'\b\w+\b', doc)]    
    vectorizer = HashingVectorizer(tokenizer=stemTokenize, ngram_range=(1, 3), token_pattern=r'\b\w+\b', stop_words='english', binary=False, norm='l2', n_features=2**19)

    anchorText = sys.argv[2]

    anchorVector = vectorizer.transform([anchorText]).toarray()
    distances = (anchorVector * trainedVectorArray.T)[0]
    nonzeroIndices = numpy.nonzero(distances)[0]
    sortedIndices = nonzeroIndices[numpy.argsort(distances[nonzeroIndices])][::-1][:int(sys.argv[3])]
    snippetCollection_id_sorted = [snippetCollection_id[index] for index in sortedIndices]

    sys.stdout.write(json.dumps(snippetCollection_id_sorted))