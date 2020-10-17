from pprint import pprint
from datetime import date, datetime
from mdutils.mdutils import MdUtils


from pprint import pprint


class Jekyllify:
    def __init__(self, publications, config):
        self._publications = publications
        self._jekyll_layout = config['jekyll-layout']
        self._output_dir = config['output-dir']
        self._author_name = config['author-name']

    def set_publications(self, publications):
        self._publications = publications

    def generate(self):
        # today = date.today()
        # date_today = today.strftime("%B %d, %Y")
        # time = now.strftime("%H:%M")

        for p in self._publications:
            md = MdUtils(
                file_name=self._output_dir + '/' + p['title'])

            md.new_line('---')  # front matter
            md.new_line('layout: ' + self._jekyll_layout)
            md.new_line('title: ' + p['title'])
            md.new_line('author: ' + self._author_name)
            # md.new_line('category: ' + p['type'])
            md.new_line('---')  # front matter

            md.new_header(level=1, title='Abstract')
            md.new_line('</br>')
            md.new_paragraph(p['abstract'])

            md.new_line('</br>')
            md.new_header(
                level=2, title='You can may use the following bibtex code to cite this work:')
            if 'bibtex' in p.keys():
                md.new_line('</br>')
                md.insert_code(p['bibtex'], language='shell')

            md.new_line('</br>')
            md.new_paragraph(
                "You can see the full publication in the following link: [" + p['url'] + "](" + p['url'] + ")")


# ---
# layout: post
# title:  "Welcome to devlopr jekyll !"
# summary: Hello World ! This is a sample post
# author: John Doe
# date: '2019-05-22 14:35:23 +0530'
# category: jekyll
# thumbnail: /assets/img/posts/code.jpg
# keywords: devlopr jekyll, how to use devlopr, devlopr, how to use devlopr-jekyll, devlopr-jekyll tutorial,best jekyll themes
# permalink: /blog/welcome-to-devlopr-jekyll
# ---

            md.create_md_file()
        # self._posts = []
        # pprint(p)

    def write(self):
        pass
