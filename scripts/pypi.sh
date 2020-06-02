!/usr/bin/env bash
# just to be safe: wipe the dist folder of previous builds
rm -r dist/*
# ensure you hav the latest versions of twine, setuptools, and wheel
python3 -m pip install --user --upgrade twine setuptools wheel
# build the package
python3 setup.py sdist bdist_wheel
# upload it to PyPI
python3 -m twine upload dist/*