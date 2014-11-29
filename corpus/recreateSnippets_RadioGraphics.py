import parser_RadioGraphics as parser
from bs4 import BeautifulSoup
from time import time
import sys
from pymongo import MongoClient


db_uri = 'mongodb://localhost:27017'
client = MongoClient(db_uri)
db = client['radsquared-dev']
corpus = db['corpus']

start = time()
sys.stdout.write("removing snippets...")
sys.stdout.flush()
corpus.remove({'source': 'RadioGraphics', 'docType': 'snippet'})
sys.stdout.write(str(time() - start) + " seconds\n")
sys.stdout.flush()

start = time()
sys.stdout.write("fetching articles...")
sys.stdout.flush()
articles = corpus.find({'source': 'RadioGraphics', 'docType': 'article'})
sys.stdout.write(str(time() - start) + " seconds\n")
sys.stdout.flush()

num_articles = articles.count()

for count, article in enumerate(articles):
    start = time()
    sys.stdout.write("article # " + str(count) + " of " + str(num_articles) + ": recreating snippets...")
    sys.stdout.flush()
    entry_url = article['sourceURL']
    entry_html_source = article['sourceHTML']        
        
    # format of returned list from get_metadata function:
    # 0 identifier
    # 1 title
    # 2 journal
    # 3 date
    # 4 authors
    # 5 publisher
    resource_metadata = parser.get_metadata(entry_url, entry_html_source)
    
    resource_id = article['_id']
    doi = article['sourceId']

    resource_snippets = []
    
    # creates resource_snippet objects of type 'figure'
    figures = parser.get_figures(entry_url, entry_html_source)
    for i, figure in enumerate(figures):
        resource_snippets.append({'docType': 'snippet',
            'docSubtype': 'figure',
            'name': figure[0],
            'content': figure[1],
            'url_small': figure[2],
            'url_medium': figure[3],
            'url_large': figure[4],
            'source': 'RadioGraphics',
            'sourceId': doi,
            'title': resource_metadata[1],
            'date': resource_metadata[3],
            'authors': resource_metadata[4],
            'publisher': resource_metadata[5],
            'sourceURL': entry_url,
            'resource_id': resource_id})
    
    # creates resource_snippet objects of type 'paragraph'
    paragraphs = parser.get_paragraphs(entry_url, entry_html_source)
    for i, paragraph in enumerate(paragraphs):
        resource_snippets.append({'docType': 'snippet',
            'docSubtype': 'paragraph',
            'name': 'paragraph ' + str(i),
            'content': paragraph,
            'source': 'RadioGraphics',
            'sourceId': doi,
            'title': resource_metadata[1],
            'date': resource_metadata[3],
            'authors': resource_metadata[4],
            'publisher': resource_metadata[5],
            'sourceURL': entry_url,
            'resource_id': resource_id})
    
    resource_snippets_id = corpus.insert(resource_snippets)
    
    sys.stdout.write(str(time() - start) + " seconds\n")
    sys.stdout.flush()
    
corpus.reindex()