:: Deploy to Pypi test site
@echo off
cd ..
python setup.py sdist upload -r pypi
pause