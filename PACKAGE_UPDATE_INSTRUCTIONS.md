# Steps on how to Update this Package in PyPi

1. Change \_equity__version\_ to the correct version in `equit_ease/main.py`.
2. run `python3 setup.py sdist bdist_wheel` to build new `dist/` folder
3. run `twine upload dist/` to upload the new package info to PyPi
**For all this to work, make sure the correct pypi environment variables are set.**