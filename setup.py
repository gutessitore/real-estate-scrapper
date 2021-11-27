from distutils.core import setup

setup(
    name='real_estate',
    packages=['real_estate'],
    version='0.0.0',
    license='MIT',
    description='Package to scrape and analise data from real estate sites in Brazil',
    author='Gustavo Schlieper Tessitore',
    author_email='gugatessi@gmail.com',
    url='https://github.com/gutessitore/real-estate-scrapper',
    download_url='https://github.com/gutessitore/real-estate-scrapper/archive/refs/tags/0.0.0.tar.gz',
    keywords=['real estate', 'rent', 'buy', 'web scrapper', 'selenium'],
    install_requires=[
        'pandas',
        'folium',
        'numpy',
        'selenium',
        'geopy',
        'tqdm',
        'pycep_correios',
        'firebase_admin'
    ]
)
