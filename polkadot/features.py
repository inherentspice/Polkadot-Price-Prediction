from data import Polkadot

class Dataframe:
    def get_coingecko(self):
        df = Polkadot().get_data().get('Coingecko')
        df.rename(columns={'Unnamed: 0': 'date'}, inplace=True)
        return df
