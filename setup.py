from distutils.core import setup
import real_estate
import os


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        if directories:
            try:
                directories.remove("__pycache__")
            except ValueError:
                pass
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths


extra_files = package_files('real_estate/src')
version = real_estate.__version__

setup(
    name='real_estate',
    packages=['real_estate'],
    package_data={'': extra_files},
    version=version,
    license='MIT',
    description='Package to scrape and analise data from real estate sites in Brazil',
    author='Gustavo Schlieper Tessitore',
    author_email='gugatessi@gmail.com',
    url='https://github.com/gutessitore/real-estate-scrapper',
    download_url=f'https://github.com/gutessitore/real-estate-scrapper/archive/refs/tags/{version}.tar.gz',
    keywords=['real estate', 'rent', 'buy', 'web scrapper', 'selenium'],
    install_requires=[
        'pandas',
        'folium',
        'numpy',
        'selenium==3.141.0',
        'geopy',
        'tqdm',
        'pycep_correios',
        'firebase_admin'
    ]
)
