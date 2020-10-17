import time
from tqdm import tqdm
from copy import deepcopy
from scholarly import scholarly, ProxyGenerator


class GScholarScrapper:
    def __init__(self, config):
        self._scholar_id = config['scholar-id']
        self._timeout = config['timeout']
        self._max_retries = config['max-retries']
        self._config = config
        self._reset_scholarly_proxy()

    def _reset_scholarly_proxy(self):
        if self._config['use-proxy']:
            if not self._config['use-tor']:
                pg = ProxyGenerator()
                pg.FreeProxies()
            else:
                pg = ProxyGenerator()
                pg.Tor_Internal(tor_cmd="tor")
            scholarly.use_proxy(pg)

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

            time.sleep(self._timeout)

            query = scholarly.search_pubs(p.bib['title'])
            bibs = next(query)

            attempts = 0
            while True:
                try:
                    bibs.fill()
                    if not isinstance(bibs, list):
                        bibs = [bibs]
                    for b in bibs:
                        if 'venue' in b.bib.keys():
                            self._formated_data[-1]['type'] = b.bib['ENTRYTYPE']
                        self._formated_data[-1]['bibtex'] = b.bibtex
                    break
                except:
                    print('Attempt ' + str(attempts) + ' -- Failed to get bibtex -- retrying in ' +
                          str(self._timeout) + ' secs')
                    attempts += 1
                    self._reset_scholarly_proxy()
                    time.sleep(self._timeout)

                if attempts > self._max_retries - 1:
                    break
            time.sleep(self._timeout)

    def get_formated_data(self):
        return self._formated_data

    def get_raw_data(self):
        return copy.deepcopy(self._data)
