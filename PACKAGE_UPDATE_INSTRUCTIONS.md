# Steps on how to Update this Package in PyPi

1. Change _equity__version_ to the correct version in `equit_ease/main.py`.
2. run `python3 setup.py sdist bdist_wheel` to build new `dist/` folder
3. run `twine upload dist/` to upload the new package info to PyPi
