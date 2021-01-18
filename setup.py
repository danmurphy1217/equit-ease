# -*- coding: utf-8 -*-

from setuptools import setup
import re

version = re.search(
    '^__version__\s+=\s+(.*)',
    open('main.py').read(),
    re.MULTILINE
).group(1)

setup(
    name="equit-ease",
    packages= ["equit_ease"],
    version= version,
    entry_points={
        "console_scripts": ['equity = main:main']
    },
    description = "The easiest way to retrieve equity data from the command line. Search Stocks, Options, Cryptocurrencies and other digital assets, and more in a manner of seconds.",
    author= "Dan Murphy",
    author_email = "danielmurph8@gmail.com",
    install_requires=[*open("requirements.txt").read().splitlines()]
)