import pandas as pd
import os

class Polkadot:
    def get_data(self, on_chain=False):
        """ This function returns a Python dict.
        If 'on_chain' is set to True, the keys should be 'Treasury Available Income',
        'Daily Unbonding Schedule (DOT), etc.
        Else it will have one key: 'Coingecko'
        Its values should be pandas.DataFrames loaded from csv files """
        data = {}

        if on_chain == True:
            csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
            file_names = [f for f in os.listdir(csv_path) if f.endswith('.csv')]
            for i, j in enumerate(file_names):
                file_names[i] = j.replace('.csv', '')
            for (x, y) in zip(file_names, os.listdir(csv_path)[1:]):
                data[x] = pd.read_csv(os.path.join(csv_path, y))

        data['Coingecko'] = pd.read_csv('Polkadot_historical_data.csv')
        return data

    # def update_coingecko(self):
    #     data = self.get_data(on_chain=False)
