from helperFunctions import pickle_zloads, pickle_zdumps
from pymongo import MongoClient
import gridfs

db_uri = 'mongodb://localhost:27017'
client = MongoClient(db_uri)
db = client['radsquared-dev']
fs = gridfs.GridFS(db)
# loads snippet ids
pklcompfile = fs.get_last_version(filename="python-data/snippetCollection_text.pkl").read()
snippetCollection_text = pickle_zloads(pklcompfile)

''' loads files from local directory
import os
# loads snippets
f = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'snippetCollection_text.pkl'), 'rb')
snippetCollection_text = pickle_zloads(f.read())
f.close()
'''

from nltk.stem.snowball import SnowballStemmer
import re
from sklearn.feature_extraction.text import HashingVectorizer
import numpy
import sys

def stemTokenize(doc):
    stemmer = SnowballStemmer('english')
    return [stemmer.stem(word) for word in re.findall(r'\b\w+\b', doc)]

vectorizer = HashingVectorizer(tokenizer=stemTokenize, ngram_range=(1, 3), token_pattern=r'\b\w+\b', stop_words='english', binary=False, norm='l2', n_features=2**19)
trainedVectorArray = vectorizer.fit_transform(snippetCollection_text)
anchorVector = vectorizer.transform([sys.argv[1]]).toarray()
distances = (anchorVector * trainedVectorArray.T)[0]
nonzeroIndices = numpy.nonzero(distances)[0]
sortedIndices = nonzeroIndices[numpy.argsort(distances[nonzeroIndices])][::-1]
for i in sortedIndices[:int(sys.argv[2])]:
    print(snippetCollection_text[i] + '\n')