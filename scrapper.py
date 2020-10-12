import time
from tqdm import tqdm
from scholarly import scholarly, ProxyGenerator

from pprint import pprint


class GScholarScrapper:
    def __init__(self, config):
        self._scholar_id = config['scholar-id']
        self._timeout = config['timeout']
        if config['use-proxy']:
            pg = ProxyGenerator()
            scholarly.use_proxy(pg.FreeProxies())

    def fetch(self):
        self._data = scholarly.search_author_id(self._scholar_id).fill()
        self._formated_data = []
        for p in tqdm(self._data.publications, desc='Going through publications'):
            p = p.fill()
            self._formated_data.append({
                'abstract': p.bib['abstract'],
                'title': p.bib['title'],
                'authors': p.bib['author'],
                'cites': p.bib['cites'],
                'url': p.bib['url'],
                'year': p.bib['year'],
                'cites_per_year': p.cites_per_year,
            })

            if 'journal' in p.bib.keys():
                self._formated_data[-1]['medium'] = p.bib['journal']
            elif 'eprint' in p.bib.keys():
                self._formated_data[-1]['medium'] = p.bib['eprint']
            else:
                self._formated_data[-1]['medium'] = p.bib['N/A']

            attempts = 0
            while True:
                try:
                    query = scholarly.search_pubs(p.bib['title'])
                    bibs = next(query).fill()
                    if not isinstance(bibs, list):
                        bibs = [bibs]
                    for b in bibs:
                        if 'venue' in b.bib.keys():
                            self._formated_data[-1]['medium'] = b.bib['venue']
                            self._formated_data[-1]['type'] = b.bib['ENTRYTYPE']
                    break
                except:
                    print('Attempt ' + str(attempts) + ' -- Failed to get bibtex -- retrying in ' +
                          str(self._timeout) + ' secs')
                    attempts += 1
                    time.sleep(self._timeout)

            time.sleep(self._timeout)

    def get_formated_data(self):
        return self._formated_data

    def get_raw_data(self):
        return self._data
