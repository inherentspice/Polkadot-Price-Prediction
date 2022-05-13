from data import Polkadot
import pandas as pd
import numpy as np
from functools import reduce


class Dataframe:
    def __init__(self):
        self.data = Polkadot().get_data()

    def get_coingecko(self):
        """This function returns a pandas DataFrame.
        It contains 9 columns of data retrieved from
        Coingecko."""
        df = self.data.get('Coingecko')
        df.rename(columns={'Unnamed: 0': 'date'}, inplace=True)
        df['date'] = pd.to_datetime(df['date'], dayfirst=True)
        return df

    def get_fear_and_greed(self):
        """This function returns a pandas DataFrame.
        It contains 3 columns: Date, Value, Value_classification.
        This data was retrieved from alternative.me Fear
        And Greed Index for Bitcoin"""
        df = self.data.get('Fear_and_greed')
        df.drop(columns='Unnamed: 0', inplace=True)
        df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
        df.rename(columns={'Date': 'date'}, inplace=True)
        df.sort_values(by='date', inplace=True)
        return df

    def get_on_chain(self):
        df = self.data.get('On_chain')
        df.drop(columns='Unnamed: 0', inplace=True)
        df['time_utc'] = pd.to_datetime(df['time_utc'], dayfirst=True)
        df['time_utc'] = df['time_utc'].dt.date
        df.rename(columns={'time_utc': 'date'}, inplace=True)
        df['date'] = pd.to_datetime(df['date'])
        return df

    def get_dataframe(self):
        gecko_df = self.get_coingecko()
        fear_df = self.get_fear_and_greed()
        on_df = self.get_on_chain()
        df = [gecko_df, fear_df, on_df]
        df_merged = reduce(lambda left,right: pd.merge(left,right,on=['date'],
                                            how='outer'), df)
        df_merged.drop(df_merged.tail(1).index,inplace=True)
        return df_merged

    def get_features(self, forecast_out=7, classification=True):
        """This function returns a pandas DataFrame with
        36 columns. It creates multiple exponential moving averages,
        and other features, to use in making a model"""
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

        #create sats changes
        features['sats_change_2_days'] = features['current_price_sats'] - features['current_price_sats'].shift(2)
        features['sats_change_1_week'] = features['current_price_sats'] - features['current_price_sats'].shift(7)
        features['sats_change_2_weeks'] = features['current_price_sats'] - features['current_price_sats'].shift(14)

        #create price changes
        features['price_change_2_days'] = features['current_price'] - features['current_price'].shift(2)
        features['price_change_1_week'] = features['current_price'] - features['current_price'].shift(7)
        features['price_change_2_weeks'] = features['current_price'] - features['current_price'].shift(14)

        #create price change as a percentage
        features['percent_change_2_days'] = features['current_price'].pct_change(periods=2)
        features['percent_change_1_week'] = features['current_price'].pct_change(periods=7)
        features['percent_change_2_weeks'] = features['current_price'].pct_change(periods=14)

        #create change in sats value as a percentage
        features['percent_sats_2_days'] = features['current_price_sats'].pct_change(periods=2)
        features['percent_sats_1_week'] = features['current_price_sats'].pct_change(periods=7)
        features['percent_sats_2_weeks'] = features['current_price_sats'].pct_change(periods=14)

        # replace null values
        features['public_interest_stats'][features['public_interest_stats'].isnull()] = 0
        features['fear_change_2_days'][features['fear_change_2_days'].isnull()] = 0
        features['fear_change_1_week'][features['fear_change_1_week'].isnull()] = 0
        features['fear_change_2_weeks'][features['fear_change_2_weeks'].isnull()] = 0
        features['reddit_change_2_days'][features['reddit_change_2_days'].isnull()] = 0
        features['reddit_change_1_week'][features['reddit_change_1_week'].isnull()] = 0
        features['reddit_change_2_weeks'][features['reddit_change_2_weeks'].isnull()] = 0
        features['sats_change_2_days'][features['sats_change_2_days'].isnull()] = 0
        features['sats_change_1_week'][features['sats_change_1_week'].isnull()] = 0
        features['sats_change_2_weeks'][features['sats_change_2_weeks'].isnull()] = 0
        features['price_change_2_days'][features['price_change_2_days'].isnull()] = 0
        features['price_change_1_week'][features['price_change_1_week'].isnull()] = 0
        features['price_change_2_weeks'][features['price_change_2_weeks'].isnull()] = 0
        features['percent_change_2_days'][features['percent_change_2_days'].isnull()] = 0
        features['percent_change_1_week'][features['percent_change_1_week'].isnull()] = 0
        features['percent_change_2_weeks'][features['percent_change_2_weeks'].isnull()] = 0
        features['percent_sats_2_days'][features['percent_sats_2_days'].isnull()] = 0
        features['percent_sats_1_week'][features['percent_sats_1_week'].isnull()] = 0
        features['percent_sats_2_weeks'][features['percent_sats_2_weeks'].isnull()] = 0
        return features
