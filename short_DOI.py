import requests
import json
import sys
import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import *

def ResolveShortDOI(doi):
    '''
    Pass a long doi through the shortdoi service and return the short doi as
    a string.
    '''
    URL = 'http://shortdoi.org/{0}?format=json'.format(doi)
    r = requests.get(URL)
    j = json.loads(r.text)


    return j['ShortDOI']

def customizations(record):
    """Use some functions delivered by the library

    :param record: a record
    :returns: -- customized record
    """
    if "bdsk-url-2" in record:
    	del record["bdsk-url-2"]
    if "bdsk-url-1" in record:
        del record["bdsk-url-1"]
    if "doi" in record:
    	doistring = record["doi"]
    	if len(doistring)>10 :
    		if 'http://dx.doi.org/' in doistring:
    			doistring = doistring.strip('http://dx.doi.org/')
    		if ResolveShortDOI(doistring):
    			link = ResolveShortDOI(doistring)
    			record["doi"] = link
    			record["link"] = 'http://doi.org' + link[2:]

    return record

with open('biblio.bib') as bibtex_file:
    parser = BibTexParser()
    parser.customization = customizations
    bibtex_database = bibtexparser.load(bibtex_file, parser=parser)

with open('bibtex.bib', 'w') as bibtex_file:
	bibtexparser.dump(bibtex_database, bibtex_file)
