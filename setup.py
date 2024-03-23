from setuptools import setup

f = open('requirements.txt', 'r')
install_requires = f.readlines()

setup(
    name='vrijopnaam-prices',
    version='0.1',
    description='Een korte beschrijving van jouw pakket',
    author='Marc Dirven',
    packages=['vrijopnaam_prices'],
    install_requires=install_requires
)
