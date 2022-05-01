import pandas as pd
import os

class Polkadot:
    def get_data(self):
        csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        file_names = [f for f in os.listdir(csv_path) if f.endswith('.csv')]
        print(file_names)

# coingecko = pd.read_csv('Polkadot_historical_data.csv')
# polkadot = pd.read_csv('../data/Daily Active Account & Newly Created Account.csv')
# print(polkadot.head())
# print(coingecko.head())
print(Polkadot().get_data())
