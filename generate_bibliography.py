#!/usr/bin/env python

import os
import yaml
import pickle
import argparse
from pathlib import Path
from jekyllify import Jekyllify
from scrapper import GScholarScrapper

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generate bibliography')
    parser.add_argument('--load', '-l', type=str,
                        help='Path to a pickle file containing stored publications',
                        default='')
    args = parser.parse_args()

    with open('config.yaml') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

    if not args.load:
        if not os.path.exists(config['output-dir']):
            os.makedirs(config['output-dir'])

    if not args.load:
        sc = GScholarScrapper(config)
        sc.fetch()
        pubs = sc.get_formated_data()
        raw = sc.get_raw_data()
        with open(Path(config['output-dir']).joinpath('articles.pkl'), 'wb') as ofile:
            pickle.dump(pubs, ofile, pickle.HIGHEST_PROTOCOL)
        if config['store-raw']:
            with open(Path(config['output-dir']).joinpath('raw_articles.pkl'), 'wb') as ofile:
                pickle.dump(raw, ofile, pickle.HIGHEST_PROTOCOL)
    else:
        basename = os.path.basename(args.load)
        dirname = os.path.dirname(args.load)
        with open(args.load, 'rb') as ifile:
            pubs = pickle.load(ifile)
        config['output-dir'] = dirname

    jk = Jekyllify(pubs, config)
    jk.generate()
