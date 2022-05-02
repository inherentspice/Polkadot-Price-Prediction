from pycoingecko import CoinGeckoAPI
import datetime
import pandas as pd
import time

# Instantiate coingeckoAPI
cg = CoinGeckoAPI()
class Scraper:
    def get_historical_data(cryptocurrency, start_date):
        """function that takes the name of a cryptocurrency and a start date (as datetime)
        and returns price (USD), price(sats), market cap, reddit posts for 48hours, reddit
        comments for 48hours, reddit subscribers for 48hours, reddit active accounts,
        and the alexa rank of the cryptocurrency for each day from the start date until
        the current date. Returns a dictionary."""

        current = datetime.datetime.today()
        dateStr = start_date.strftime("%d-%m-%Y")
        result = {}
        c = 0
        while start_date < current:

        #sleep function so that the function doesn't get blocked from the coingecko API

            if c != 0 and c % 40 == 0:
                time.sleep(65)
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
        df = pd.DataFrame.from_dict(prices, orient='index')
        df.to_csv(r'Polkadot_historical_data.csv', header=True)
        return


# call function and store dictionary in 'prices'
# prices = get_historical_data('polkadot', pd.to_datetime('19-08-2020'))

# convert dictionary to a DataFrame and write it into a csv file
# df = pd.DataFrame.from_dict(prices, orient='index')
# df.to_csv (r'Polkadot_historical_data.csv', header=True)
