'''
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
HTML Parser 
RadioGraphics

(c) 2014 L. Leon Chen
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

import re
from bs4 import BeautifulSoup

'''
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
get_metadata

Returns metadata, which is a list of the following:
0 identifier
1 title
2 journal
3 date
4 authors
5 publisher
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''
def get_metadata(url, entry_html_source):
    soup = BeautifulSoup(entry_html_source, 'html.parser')
            
    meta_tags = soup.find_all('meta')
    metadata = ['']*6
    
    for meta_tag in meta_tags:    
        try:
            if 'dc.identifier' in meta_tag['name'].lower():
                if 'doi' in meta_tag['scheme'].lower():
                    metadata[0] = meta_tag['content']
                    break
        except: pass
    
    for meta_tag in meta_tags:    
        try:
            if 'dc.title' in meta_tag['name'].lower():
                metadata[1] = meta_tag['content']
                break
        except: pass
    
    metadata[2] = 'RadioGraphics'
    
    for meta_tag in meta_tags:    
        try:
            if 'dc.date' in meta_tag['name'].lower():
                metadata[3] = meta_tag['content']
                break
        except: pass
        
    authors = ''
    for meta_tag in meta_tags:
        try:
            if meta_tag['name'].lower() == 'dc.creator':
                authors += meta_tag['content'] + '; '
        except: pass
    metadata[4] = authors
    
    for meta_tag in meta_tags:    
        try:
            if 'dc.publisher' in meta_tag['name'].lower():
                metadata[5] = meta_tag['content']
                break
        except: pass
    
    return metadata

'''
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Returns figures as a list of tuples
Tuple contains:
- figure name
- figure caption
- figure small pic URL
- figure medium pic URL (may return 404)
- figure large pic URL (may return 404)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''            
def get_figures(url, entry_html_source):
    soup = BeautifulSoup(entry_html_source, 'html.parser')
    figure_list = []    
    url_base = 'http://pubs.rsna.org'
    figures = soup.find_all(id=re.compile('(^F\d)|(^fig\d\d$)'))
    for figure in figures:
        name = figure['id']    
        try:
            caption = figure.text
        except: pass
        for fig in figure.find_all('img'):
            smallpic_url = url_base + fig['src']
            mediumpic_url = smallpic_url.replace('gif','jpeg').replace('small','medium')
            largepic_url = smallpic_url.replace('gif','jpeg').replace('small','large')
            figure_list_item = name, caption, smallpic_url, mediumpic_url, largepic_url
            figure_list.append(figure_list_item)
    return figure_list

'''
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Returns content paragraphs
(Discards figure and tables with captions; these are produced by
    separate functions)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''    
def get_paragraphs(url, entry_html_source):
    soup = BeautifulSoup(entry_html_source, 'html.parser')
    if soup.article is not None:
        soup = soup.article
    paragraph_list = []
    nonrelevant = soup.find_all(class_='NLM_sec-type_intro')
    for sec in nonrelevant:
        try:
            sec.decompose()
        except: pass
    nonrelevant = soup.find_all(class_='NLM_fn')
    for sec in nonrelevant:
        try:
            sec.decompose()
        except: pass
    refs = soup.find_all(class_='ref')
    for ref in refs:
        try:
            ref.decompose()
        except: pass
    figs = soup.find_all(id=re.compile('(^F\d)|(^fig\d\d$)'))
    for fig in figs:
        try:
            fig.decompose()
        except: pass
    tables = soup.find_all(id=re.compile('(^t\d\d$)|(^div-t\d\d$)'))
    for t in tables:
        try:
            t.decompose()
        except: pass
    footnotes = soup.find_all(class_='footnote')
    for fn in footnotes:
        try:
            fn.decompose()
        except: pass
    paragraphs = soup.find_all('p')
    for paragraph in paragraphs:
        try:
            paragraph = paragraph.text
            paragraph = re.compile('(\(\))|(\(,\))|(\(,,\))|(\(,,,\))|(\(\u2013\))|( \(\))|( \(,\))|( \(,,\))|( \(,,,\))|( \(\u2013\))').sub('', paragraph)
            if not (paragraph == ''):
                paragraph_list.append(paragraph)
        except: pass
    return paragraph_list