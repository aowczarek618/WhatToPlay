from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='xgp-reccomender',
    version='1.0.0',
    description='App searches for avaiable Xbox Game Pass games and helps to choose what to play next.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/aowczarek618/xgp-reccomender',
    packages=find_packages(where='.'),
    python_requires='>=3.5, <4',
    install_requires=['requests', 'beautifulsoup4', 'pandas'],
    project_urls={
        'Bug Reports': 'https://github.com/aowczarek618/xgp-reccomender/issues',
        'Source': 'https://github.com/aowczarek618/xgp-reccomender',
    },
)