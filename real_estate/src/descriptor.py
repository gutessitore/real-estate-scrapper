from sklearn.cluster import KMeans
import pandas as pd
from real_estate.src.errors import InvalidDataFrameError


class RentStats:
    def __init__(self, df: pd.DataFrame):
        if list(df.columns) != ['banheiros', 'distância', 'endereço', 'img1', 'lat', 'link', 'lon', 'preço', 'quartos',
                                'site', 'texto', 'área', 'vagas', 'valor_de_condominio']:
            raise InvalidDataFrameError("O DataFrame que você passou precisa vir diretamente do Collector.\
             \nSe você já está usando o Collector, você não se esqueceu de acessar os dados com o .data?")
        self._df = df
        self._model = None


    def get_min_prices(self, k=5):
        """
        Returns the k lowest price announcements
        :return DataFrame
        """
        return self._df.loc[:k - 1, 'preço'].sort_values(ascending=True).reset_index(drop=True)

    def get_max_prices(self, k):
        """
        Returns the k highest price announcements
        :return DataFrame
        """
        return self._df.loc[:k - 1, 'preço'].sort_values(ascending=False).reset_index(drop=True)
        # return self._df.sort_values(by="preço", ascending=False).reset_index(drop=True)

    def get_best_ratio(self, ascending=True):
        """
        Returns a DataFrame ordered by price/m² ratio
        :return DataFrame
        """
        self._df['p/m2'] = self._df['preço'] / self._df['área']
        return self._df.sort_values(by="p/m2", ascending=ascending).reset_index(drop=True)

    def get_best_dist(self, ascending=True):
        """
        Return a DataFrame ordered by distance
        :return DataFrame
        """
        return self._df.sort_values(by='distância', ascending=ascending).reset_index(drop=True)

    @property
    def _to_quantitative(self):
        return self._df._get_numeric_data().copy()

    def clusterize(self, number_of_clusters: int, random_state: int = None):

        quantitative_df = self._to_quantitative
        train_data = quantitative_df.fillna(0).to_numpy()

        self._model = KMeans(
            n_clusters=number_of_clusters,
            random_state=random_state
        )

        self._model.fit(train_data)
        predicted_data = self._model.predict(train_data)

        self._df["cluster"] = [i for i in predicted_data]

    @property
    def data(self):
        return self._df

