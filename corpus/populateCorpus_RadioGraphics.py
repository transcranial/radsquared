'''
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Populate Corpus
RadioGraphics

Uses the mechanize to simulate a browser and extract html from 
article webpages. The html data are then parsed and stored in 
the database.

(c) 2014 L. Leon Chen
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

import parser_RadioGraphics as parser
from identifiers_RadioGraphics import doi_list
import requests
from bs4 import BeautifulSoup
from time import time, sleep
import sys
from pymongo import MongoClient


db_uri = 'mongodb://heroku_app24877560:c7ppvded5f65vlk3vpkk823gce@ds043259-a0.mongolab.com:43259/heroku_app24877560'
client = MongoClient(db_uri)
db = client['heroku_app24877560']
corpus = db['corpus']


def populateCorpus(startIndex, endIndex):

    startIndex = int(startIndex)
    endIndex = int(endIndex)

    num_articles = len(doi_list)
    doi_already_in_db = []
    for article in corpus.find({'source': 'RadioGraphics', 'docType': 'article'}):
        doi_already_in_db.append(article['sourceId'])
    doi_already_processed = []

    for count, doi in enumerate(doi_list[startIndex:endIndex]):

        sleep(60)
        
        if doi in doi_already_in_db:
            doi_already_processed.append(doi)
            print("article # " + str(count+startIndex) + " already in db")
            continue
        if doi in doi_already_processed:
            print("article # " + str(count+startIndex) + " already processed")
            continue
        
        url = 'http://pubs.rsna.org/doi/full/%s' % doi
        try:
            sys.stdout.write("article # " + str(count+startIndex) + " of " + str(num_articles) + ": reading url...")
            sys.stdout.flush()
            while True:
                start = time()
                r = requests.get(url)
                requestError = r.status_code != 200
                if not requestError:
                    break
                else:
                    sys.stdout.write("error code " + str(r.status_code) + ", waiting...")
                    sys.stdout.flush()
                    sleep(7200)
            entry_url = r.url
            entry_html_source = r.text
            soup = BeautifulSoup(entry_html_source, 'html.parser')
            is_not_free = soup.find(id='accessDenialWidget')
            if is_not_free is not None:
                sys.stdout.write(str(time() - start) + " seconds")
                sys.stdout.write("...skipping, article not free.\n")
                sys.stdout.flush()
            else:
                sys.stdout.write("adding to database...")
                sys.stdout.flush()
                
                # format of returned list from get_metadata function:
                # 0 identifier
                # 1 title
                # 2 journal
                # 3 date
                # 4 authors
                # 5 publisher
                resource_metadata = parser.get_metadata(entry_url, entry_html_source)
                
                # creates resource objects
                resource = {'docType': 'article',
                    'source': 'RadioGraphics',
                    'sourceId': doi,
                    'title': resource_metadata[1],
                    'date': resource_metadata[3],
                    'authors': resource_metadata[4],
                    'publisher': resource_metadata[5],
                    'sourceURL': entry_url,
                    'sourceHTML': entry_html_source}
                resource_id = corpus.insert(resource)
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
            
            doi_already_processed.append(doi)
        
        except:
            print("Failed. Unexpected error:", sys.exc_info()[0])

'''
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
__main__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''   
if __name__ == '__main__':
    populateCorpus(sys.argv[1], sys.argv[2])