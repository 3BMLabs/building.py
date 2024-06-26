Steps to build Building.py package
Create package: python setup.py sdist bdist_wheel
Test local: pip install dist/{file}.whl
Publish package: twine upload dist/*