from pycoingecko import CoinGeckoAPI
import datetime
import pandas as pd
import time
import requests
import json
from functools import reduce



class Scraper:
    def get_historical_data(self, cryptocurrency, start_date, update=False):
        """function that takes the name of a cryptocurrency and a start date (as datetime)
        and returns price (USD), price(sats), market cap, reddit posts for 48hours, reddit
        comments for 48hours, reddit subscribers for 48hours, reddit active accounts,
        and the alexa rank of the cryptocurrency for each day from the start date until
        the current date. Returns a dictionary."""

        # Instantiate coingeckoAPI

        cg = CoinGeckoAPI()
        current = datetime.datetime.today()
        dateStr = start_date.strftime("%d-%m-%Y")
        result = {}
        c = 0
        while start_date < current:

        #sleep function so that the function doesn't get blocked from the coingecko API

            if c != 0 and c % 40 == 0:
                print('Wait one minute')
                time.sleep(70)

            dateStr = start_date.strftime("%d-%m-%Y")
            historic = cg.get_coin_history_by_id(cryptocurrency, date=dateStr, localization='false')
            result[dateStr] = {'current_price':historic.get('market_data').get('current_price').get('usd'),
                       'current_price_sats':historic.get('market_data').get('current_price').get('sats'),
                       'market_cap':historic.get('market_data').get('market_cap').get('usd'),
                       'reddit_post_48h':historic.get('community_data').get('reddit_average_posts_48h'),
                       'reddit_comment_48h':historic.get('community_data').get('reddit_average_comments_48h'),
                       'reddit_subscribers':historic.get('community_data').get('reddit_subscribers'),
                       'reddit_active_accounts':historic.get('community_data').get('reddit_accounts_active_48h'),
                       'public_interest_stats':historic.get('public_interest_stats').get('alexa_rank')}
            start_date += datetime.timedelta(days=1)
            c += 1
            print(f'{dateStr} processed')
        df = pd.DataFrame.from_dict(result, orient='index')
        if update == True:
            return df
        df.to_csv(r'Polkadot_historical_data.csv', header=True)
        return

    def get_fear_and_greed(self, limit=622):
        url = f"https://api.alternative.me/fng/?limit={limit}&date_format=cn"
        api_data = requests.get(url).json()
        df = pd.DataFrame(columns=['Date', 'Value', 'Value_classification'])
        for i in api_data['data']:
            timestamp = i.get('timestamp')
            value = i.get('value')
            value_classification = i.get('value_classification')
            df.loc[df.shape[0]] = {'Date':timestamp, 'Value':value, 'Value_classification':value_classification}
        df.to_csv(r'Bitcoin_fear_and_greed.csv', header=True)
        return

    def get_on_chain(self, start_date):
        """function that takes  a start date (as string in format [year-month-day]
        and returns daily fees, active accounts, and new accounts for each day from the start date until
        the current date. Writes to a csv file."""

        API = 'xx'
        url = 'https://polkadot.api.subscan.io/api/scan/daily'
        end_date = datetime.datetime.today()
        end_date = end_date.strftime("%Y-%m-%d")
        headers = {'Content-Type' : 'application/json',
                   'X-API-Key': API}
        data_new= {"start": start_date,
                   "end": end_date,
                   "format": "day",
                   "category": "NewAccount"}

        new_string = json.dumps(data_new)

        response_new = requests.post(url, headers=headers,
                                 data=new_string).json()

        data_active={"start": start_date,
                     "end": end_date,
                     "format": "day",
                     "category": "ActiveAccount"}
        active_string = json.dumps(data_active)
        response_active = requests.post(url, headers=headers, data=active_string).json()

        data_fees={"start": start_date,
                   "end": end_date,
                   "format": "day",
                   "category": "transfer"}
        fees_active = json.dumps(data_fees)

        response_fees = requests.post(url, headers=headers, data=fees_active).json()
        df_new = pd.DataFrame(response_new['data']['list'])
        df_new = df_new[['time_utc', 'total']]
        df_new.rename({'total':'new_accounts'}, inplace=True)

        df_active = pd.DataFrame(response_active['data']['list'])
        df_active = df_active[['time_utc', 'total']]
        df_active.rename({'total':'active_accounts'}, axis=1, inplace=True)

        df_fees = pd.DataFrame(response_fees['data']['list'])
        df_fees = df_fees[['time_utc', 'total']]
        df_fees.rename({'total': 'fees'}, axis=1, inplace=True)

        df = [df_new, df_active, df_fees]
        df_merged = reduce(lambda  left,right: pd.merge(left,right,on=['time_utc'],
                                            how='outer'), df)
        df_merged.to_csv(r'Polkadot_on_chain_data.csv', header=True)
        return

# Scraper().get_fear_and_greed()
# Scraper().get_historical_data('polkadot', pd.to_datetime('19-08-2020'))
# Scraper().get_on_chain('2020-08-19')
