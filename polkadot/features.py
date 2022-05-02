from data import Polkadot
import pandas as pd

class Dataframe:
    def get_coingecko(self):
        df = Polkadot().get_data().get('Coingecko')
        df.rename(columns={'Unnamed: 0': 'date'}, inplace=True)
        df['date'] = pd.to_datetime(df['date'])
        return df
