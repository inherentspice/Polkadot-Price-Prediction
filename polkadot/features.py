from data import Polkadot
import pandas as pd

class Dataframe:
    def get_coingecko(self):
        df = Polkadot().get_data().get('Coingecko')
        df.rename(columns={'Unnamed: 0': 'date'}, inplace=True)
        df['date'] = pd.to_datetime(df['date'])
        return df

    def get_fear_and_greed(self):
        df = Polkadot().get_data().get('Fear_and_greed')
        df.drop(columns='Unnamed: 0', inplace=True)
        df['Date'] = pd.to_datetime(df['Date'])
        df['Value_classification'] = df['Value_classification'].astype("str")
        df.sort_values(by='Date', inplace=True)
        return df
