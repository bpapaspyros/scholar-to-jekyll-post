#!/usr/bin/env python

import yaml
import pickle
import argparse
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
        sc = GScholarScrapper(config).fetch()
        fdata = sc.get_formated_data()
        with open('articles.pkl', 'wb') as ofile:
            pickle.dump(fdata, ofile, pickle.HIGHEST_PROTOCOL)
    else:
        with open('articles.pkl', 'rb') as ifile:
            fdata = pickle.load(ifile)
