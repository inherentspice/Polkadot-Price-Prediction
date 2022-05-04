from data import Polkadot
import pandas as pd
import numpy as np

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

    def get_features_targets(self, forecast_out=2, classification=True):
        features = self.get_dataframe()

        # create target
        features['predict'] = features['current_price'].shift(-forecast_out)
        if classification == True:
            features['predict'] = pd.Series(np.where(features['predict'].values < features['current_price'], 0, 1),
                                            features.index)

        # create features
        # create price exponential moving averages
        features['price_ema5'] = features['current_price'].ewm(span=5, adjust=False).mean()
        features['price_ema20'] = features['current_price'].ewm(span=20, adjust=False).mean()
        features['price_ema50'] = features['current_price'].ewm(span=50, adjust=False).mean()

        # create fear and greed moving averages
        features['fear_ema5'] = features['Value'].ewm(span=2, adjust=False).mean()
        features['fear_ema20'] = features['Value'].ewm(span=20, adjust=False).mean()
        features['fear_ema50'] = features['Value'].ewm(span=50, adjust=False).mean()

        # create fear and greed changes
        features['fear_change_2_days'] = features['Value'] - features['Value'].shift(2)
        features['fear_change_1_week'] = features['Value'] - features['Value'].shift(7)
        features['fear_change_2_weeks'] = features['Value'] - features['Value'].shift(14)

        # create reddit posts moving averages
        features['reddit_post_ema5'] = features['reddit_post_48h'].ewm(span=5, adjust=False).mean()
        features['reddit_post_ema20'] = features['reddit_post_48h'].ewm(span=20, adjust=False).mean()
        features['reddit_post_ema50'] = features['reddit_post_48h'].ewm(span=50, adjust=False).mean()

        #create reddit changes
        features['reddit_change_2_days'] = features['reddit_post_48h'] - features['reddit_post_48h'].shift(2)
        features['reddit_change_1_week'] = features['reddit_post_48h'] - features['reddit_post_48h'].shift(7)
        features['reddit_change_2_weeks'] = features['reddit_post_48h'] - features['reddit_post_48h'].shift(14)

        #create value in sats moving average
        features['sats_ema5'] = features['current_price_sats'].ewm(span=5, adjust=False).mean()
        features['sats_ema20'] = features['current_price_sats'].ewm(span=20, adjust=False).mean()
        features['sats_ema50'] = features['current_price_sats'].ewm(span=50, adjust=False).mean()

        #create sata changes
        features['sats_change_2_days'] = features['current_price_sats'] - features['current_price_sats'].shift(2)
        features['sats_change_1_week'] = features['current_price_sats'] - features['current_price_sats'].shift(7)
        features['sats_change_2_weeks'] = features['current_price_sats'] - features['current_price_sats'].shift(14)

        #create price changes
        features['price_change_2_days'] = features['current_price'] - features['current_price'].shift(2)
        features['price_change_1_week'] = features['current_price'] - features['current_price'].shift(7)
        features['price_change_2_weeks'] = features['current_price'] - features['current_price'].shift(14)

        features.dropna(inplace=True)
        return features
