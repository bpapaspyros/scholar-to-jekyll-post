from pprint import pprint
from datetime import date, datetime


class Jekyllify:
    def __init__(self, publications, config):
        self._publications = publications
        self._jekyll_layout = config['jekyll-layout']
        self._output_dir = config['output-dir']
        self._author_name = config['author-name']

    def set_publications(self, publications):
        self._publications = publications

    def generate(self):
        today = date.today()
        date_today = today.strftime("%d-%m-%Y-")
        # time = now.strftime("%H:%M")

        for p in self._publications:
            if 'type' not in p.keys():
                p['type'] = ''
            ttl = '---\n' + \
                'layout: ' + str(self._jekyll_layout) + '\n' \
                'title: ' + str(p['title']) + '\n' \
                'author: ' + str(self._author_name) + '\n' \
                'category: ' + p['type'] + '\n' \
                'authors: ' + p['authors'] + '\n' \
                'medium: ' + p['medium'] + '\n' \
                'year: ' + p['year'] + '\n' \
                'data: ' + date_today + '\n' \
                '---\n\n'  # front matter

            body = '# Abstract \n' \
                '' + p['abstract'] + '\n'

            if 'bibtex' in p.keys():
                body += '\nYou may use the following bibtex code to cite this work:\n' \
                    '\n```shell\n' \
                    '' + p['bibtex'] + '\n```\n'

            body += '\n' \
                "You can see the full publication in the following link: [" + \
                p['url'] + "](" + p['url'] + ")"

            with open(self._output_dir + '/' + date_today + p['title'] + '.md', 'w') as ofile:
                ofile.write(ttl)
                ofile.write(body)
