Steps to build Building.py package
Create package: run 'python setup.py sdist bdist_wheel' from this folder
Test local: pip install dist/{file}.whl
Publish package: twine upload dist/*