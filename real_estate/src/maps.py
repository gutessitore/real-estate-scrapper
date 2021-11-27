from folium import plugins
import pandas as pd
import numpy as np
import folium


class Map:
    def __init__(self, data: pd.DataFrame):
        lat = data.lat.sum()/len(data)
        lon = data.lon.sum()/len(data)
        self.map = folium.Map(location=[lat, lon], zoom_start=13)

    def print(self):
        return self.map


class LocationsMap(Map):
    def __init__(self, data):
        super().__init__(data)
        first_sixth = np.quantile(data['preço'], 1 / 6)
        last_sixth = np.quantile(data['preço'], 5 / 6)

        ziped_data = zip(
            data['lat'], data['lon'], data['preço'],
            data['quartos'], data['banheiros'],
            data['vagas'], data['área'], data['link'], data['img1']
        )

        for lat, lon, preco, n_quartos, n_banheiros, n_vagas, area, link, img in ziped_data:
            html = f'''
            <img src="{img}" alt="Foto anúncio" style="width:100%;">
            <table id="vertical-1" class="centerTable">
              <tr>
                <th>Aluguel</th>
                <td>R$ {preco},00</td>
              </tr>
              <tr>
                <th>Quartos</th>
                <td>{n_quartos}</td>
              </tr>
              <tr>
                <th>Banheiros</th>
                <td>{n_banheiros}</td>
              </tr>
              <tr>
                <th>Vagas</th>
                <td>{n_vagas}</td>
              </tr>
              <tr>
                <th>Área</th>
                <td>{area} m²</td>
              </tr>
            </table>
            <div style="text-align:center">
                <a href="{link}">link</a>
            </div>'''
            iframe = folium.IFrame(html,
                                   width=250,
                                   height=400)
            popup = folium.Popup(iframe)
            if preco <= first_sixth:
                color = "green"
            elif preco < last_sixth:
                color = "orange"
            else:
                color = "red"
            folium.Marker(
                location=[lat, lon],
                popup=popup,
                icon=folium.Icon(icon="building", prefix="fa", color=color),
            ).add_to(self.map)


class HeatMap(Map):
    def __init__(self, data):
        # Remove the announcements with the same location
        data = data.groupby(by=['lat', 'lon'])['preço'].mean().reset_index()
        super().__init__(data)
        heat_data = zip(
            data['lat'], data['lon'], data['preço']
        )
        heat_map = folium.plugins.HeatMap(heat_data, name=None, min_opacity=0.5, gradient=None, overlay=True,
                                          control=True, show=True)
        heat_map.add_to(self.map)
