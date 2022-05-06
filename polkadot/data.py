import pandas as pd
import os
from coingecko_scraper import Scraper
import csv

class Polkadot:
    def get_data(self):
        """ This function returns a Python dict.
        It will have two keys: 'Coingecko', 'Fear_and_greed'
        Its values should be pandas.DataFrames loaded from csv files """
        data = {}

        data['Coingecko'] = pd.read_csv('Polkadot_historical_data.csv')
        data['Fear_and_greed'] = pd.read_csv('Bitcoin_fear_and_greed.csv')
        return data
