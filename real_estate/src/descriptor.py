import pandas as pd


class RentStats:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def get_min_price(self):
        """
        Returns the k lowest price announcements
        :return DataFrame
        """
        return self.df.sort_values(by="preço", ascending=True).reset_index(drop=True)

    def get_max_price(self):
        """
        Returns the k highest price announcements
        :return DataFrame
        """
        return self.df.sort_values(by="preço", ascending=False).reset_index(drop=True)

    def get_best_ratio(self, ascending=True):
        """
        Returns a DataFrame ordered by price/m² ratio
        :return DataFrame
        """
        self.df['p/m2'] = self.df['preço'] / self.df['área']
        return self.df.sort_values(by="p/m2", ascending=ascending).reset_index(drop=True)

    def get_best_dist(self, ascending=True):
        """
        Return a DataFrame ordered by distance
        :return DataFrame
        """
        return self.df.sort_values(by='distância', ascending=ascending).reset_index(drop=True)
