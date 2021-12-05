#### CDIA 2021-2
# Real Estate Scraper
### Framework for rental advertisement collection and analysis

#### [Github](https://github.com/gutessitore/real-estate-scrapper) |  [PyPi](https://pypi.org/project/real-estate/)


<details open="open">
  <summary>Summary</summary>
  <ol>
    <li>
      <a href="#about">About</a>
      <ul>
        <li><a href="#motivation">Motivation</a></li>
        <li><a href="#goals">Goals</a></li>
      </ul>
    </li>
    <li>
      <a href="#installation">Installation </a>
    </li>
    <li>
        <a href="#how-to-use">How to use </a>
    </li>
  </ol>
</details>

<!-- ABOUT -->
## About
>*This is a second-semester college project from students in the Data Science and Artificial Intelligence course at the Pontifical Catholic University of São Paulo (PUC-SP)*
<!-- MOTIVATION -->
### Motivation
Many of us, despite studying at PUC, live far from São Paulo. With the return of in-person activities, a big problem that we would all have to face emerged: finding a good place to live in São Paulo.

There are many websites that advertise properties for rent. In order to find a good offer, the user is required, in addition to browsing several sites, to pay attention to several variables, such as the distance from the desired location, the price of the property (plus the condominium, if any; plus taxes and fees). It is very hard work that can be automated.

This gave us the opportunity to use our programming and statistical knowledge acquired during the course to provide the user with tools that facilitate this process and also contribute to the community, since there are not many projects to solve this problem in Brazil.

<!-- GOALS -->
### Goals
Our goal was initially to extract rental advertisements from 3 websites: trovit, zapimoveis, vivareal. These ads are scraped and saved to a database, but can also be saved to a local CSV file.

After the scraping, each scraper delivers a standard output with the information of each ad following the model below:
```python
[
{"preço": 123, "endereço": "abc", "vagas": 123, "área": 123, "quartos": 123, "banheiros": 123, "link": "VivaReal", "img1": 'imagem'},
{"preço": 123, "endereço": "abc", "vagas": 123, "área": 123, "quartos": 123, "banheiros": 123, "link": "Trovit", "img1": 'imagem'},
]
```

With that, we planned provide the user some features.

First, a module which we call *RentStats*, which facilitates access to basic statistics about the data, without requiring the user to have knowledge of Pandas.

Second, a form of spatial visualization. We did this by providing two classes: *LocationsMap* and *HeatMap*.

<table>
  <tr>
    <th style="text-align:center">LocationsMap</th>
    <th style="text-align:center">HeatMap</th>
  </tr>
  <tr>
    <td><img src="https://i.imgur.com/Vx2m7ji.png"></td>
    <td><img src="https://i.imgur.com/L33NRH2.png"></td>
  </tr>
</table>

In *LocationsMap*, each dot represents a rental ad, and the color of the markers represents how expensive that rental price is relative to all other rentals in the view.

In *HeatMap* we make the relative representation of prices as a heat map.

<!-- INSTALLATION -->
## Installation

```python
# Requires Python >= 3.8
pip install real_estate
```

<!-- HOW TO USE -->
## How to Use
```python
# Importing the Collector
from real_estate import Collector
```

```python
# Collecting the data
extractor = Collector('/path/to/chromedriver', "Perdizes, São Paulo")  # Example Address
extractor.collect_data()
```

```python
# Creating a DataFrame
df = extractor.data
```

```python
# Plotting LocationsMap map
from real_estate import LocationsMap
map1 = LocationsMap(df)
map1.print()
# The map is showed in the output
```