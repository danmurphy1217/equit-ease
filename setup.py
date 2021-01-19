# -*- coding: utf-8 -*-

import setuptools

# import re
# version = re.search(
#     '^__version__\s+=\s+(.*)',
#     open('main.py').read(),
#     re.MULTILINE
# ).group(1)


long_description = open("README.md").read()


setuptools.setup(
    name="EquitEase",
    version= '0.0.3',
    url="https://github.com/danmurphy1217/equit-ease",
    entry_points={
        "console_scripts": ['equity=equit_ease.main:run']
    },
    description = "The easiest way to retrieve equity data from the command line. Search Stocks, Options, Cryptocurrencies and other digital assets, and more in a manner of seconds.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author= "Dan Murphy",
    author_email = "danielmurph8@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages= setuptools.find_packages(),
    install_requires = ['appdirs==1.4.4', 'attrs==20.3.0', 'autopep8==1.5.4', 'black==20.8b1', 'certifi==2020.12.5', 'chardet==4.0.0', 'click==7.1.2', 'docutils==0.16', 'idna==2.10', 'iniconfig==1.1.1', 'mypy-extensions==0.4.3', 'packaging==20.8', 'pathspec==0.8.1', 'pluggy==0.13.1', 'prompt-toolkit==1.0.14', 'py==1.10.0', 'pycodestyle==2.6.0', 'Pygments==2.7.4', 'PyInquirer==1.0.3', 'pyparsing==2.4.7', 'regex==2020.11.13', 'requests==2.25.1', 'rstcheck==3.3.1', 'six==1.15.0', 'toml==0.10.2', 'typed-ast==1.4.2', 'typing-extensions==3.7.4.3', 'urllib3==1.26.2', 'wcwidth==0.2.5'],
    python_requires = ">= 3.7"
)

