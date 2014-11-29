'''
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Process Corpus

Performs processing of text data using NLP methods.
Saves the vectorizer and the trained vector array as compressed+pickled files.

(c) 2014 L. Leon Chen
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

from helperFunctions import pickle_zloads, pickle_zdumps
from pymongo import MongoClient
import gridfs
import os
from time import time
from sklearn.feature_extraction.text import HashingVectorizer

from nltk.stem.snowball import SnowballStemmer
import re

def stemTokenize(doc):
    stemmer = SnowballStemmer('english')
    return [stemmer.stem(word) for word in re.findall(r'\b\w+\b', doc)]


'''
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
processCorpus
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''    
start = time()
print('reading snippets from db...')
snippetCollection_id = []
snippetCollection_text = []
db_uri = 'mongodb://localhost:27017'
client = MongoClient(db_uri)
db = client['radsquared-dev']
corpus = db['corpus']
for snippet in corpus.find({'docType': 'snippet'}):
    if len(snippet['content']) > 100:
        snippetCollection_id.append(str(snippet['_id']))
        snippetCollection_text.append(snippet['content'])
print('...', time() - start, 'sec')

fs = gridfs.GridFS(db)

# saves snippets info
start = time()
print('saving snippets info to pickled files in MongoDB...')
pklcompfile = pickle_zdumps(snippetCollection_id)
mongofile = fs.put(pklcompfile, filename="python-data/snippetCollection_id.pkl")
pklcompfile = pickle_zdumps(snippetCollection_text)
mongofile = fs.put(pklcompfile, filename="python-data/snippetCollection_text.pkl")
print('...', time() - start, 'sec')

start = time()
print('setting up vectorizer...')    
vectorizer = HashingVectorizer(tokenizer=stemTokenize, ngram_range=(1, 3), token_pattern=r'\b\w+\b', stop_words='english', binary=False, norm='l2', n_features=2**19)
print('...', time() - start, 'sec')

start = time()
print('training vectorizer and saving to pickled file in MongoDB...')
trainedVectorArray = vectorizer.fit_transform(snippetCollection_text)
# saves vector array trained on corpus
pklcompfile = pickle_zdumps(trainedVectorArray)
mongofile = fs.put(pklcompfile, filename="python-data/trainedVectorArray.pkl")
print('...', time() - start, 'sec')

'''
# saves to local directory
f = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'snippetCollection_id.pkl'), 'wb')
f.write(pickle_zdumps(snippetCollection_id))
f.close()
f = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'snippetCollection_text.pkl'), 'wb')
f.write(pickle_zdumps(snippetCollection_text))
f.close()
f = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'trainedVectorArray.pkl'), 'wb')
f.write(pickle_zdumps(trainedVectorArray))
f.close()
'''