Steps to build Building.py package

Automatically:
run pypi/test.py

Manual:

Create package: run 'python pypi/setup.py sdist bdist_wheel' from the main folder
Test local: pip install pypi/dist/{file}.whl
Publish package: twine upload pypi/dist/*