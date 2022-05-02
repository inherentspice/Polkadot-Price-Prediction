from data import Polkadot
import pandas as pd

class Dataframe:
    def __init__(self):
        self.data = Polkadot().get_data()

    def get_coingecko(self):
        df = self.data.get('Coingecko')
        df.rename(columns={'Unnamed: 0': 'date'}, inplace=True)
        df['date'] = pd.to_datetime(df['date'])
        return df

    def get_fear_and_greed(self):
        df = self.data.get('Fear_and_greed')
        df.drop(columns='Unnamed: 0', inplace=True)
        df['Date'] = pd.to_datetime(df['Date'])
        df.sort_values(by='Date', inplace=True)
        return df

    def get_dataframe(self):
        gecko_df = self.get_coingecko()
        fear_df = self.get_fear_and_greed()
        df_merged = gecko_df.merge(fear_df, left_on='date', right_on='Date')
        df_merged.drop(columns='Date', inplace=True)
        return df_merged
