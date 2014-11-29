import parser_RadioGraphics as parser

test_html = []
filenames = ['test1.html', 'test2.html', 'test3.html']
for filename in filenames:
    f = open(filename, 'r')
    test_html.append(f.read())
    f.close()

text_collection = []
for html in test_html:
    metadata = parser.get_metadata('test', html)
    for item in metadata:
        print(item, '\n')
    figures = parser.get_figures('test', html)
    for item in figures:
        print(item, '\n')
        text_collection.append(item[1])
    paragraphs = parser.get_paragraphs('test', html)
    for item in paragraphs:
        print(item, '\n')
        text_collection.append(item)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.metrics.pairwise import pairwise_distances
import numpy

vectorizer = HashingVectorizer(ngram_range=(1, 3), token_pattern=r'\b\w+\b', stop_words='english', binary=True)
trainedVectorArray = vectorizer.fit_transform(textCollection)
anchorVector = vectorizer.transform(['there is cortical thickening with a calcified nidus']).toarray()
distances = 1 - pairwise_distances(anchorVector, trainedVectorArray, 'cosine')[0]
nonzeroIndices = numpy.nonzero(distances)[0]
sortedIndices = nonzeroIndices[numpy.argsort(distances[nonzeroIndices])][::-1]
for i in sortedIndices[:10]:
    print(text_collection[i] + '\n')
'''