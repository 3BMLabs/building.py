import os
from setuptools import setup, find_packages
import shutil
from info import version_string
#copy buildingpy.py
shutil.copyfile('../BuildingPy.py', 'buildingpy/buildingpy.py')
shutil.copyfile('../LICENSE', 'LICENSE')

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


#finally, convert to package
setup(
    name='buildingpy',
    version=version_string,
    packages=find_packages(),
    description="BIM for python",
    author="3BM",
    author_email="info@3bm.co.nl",
    url="https://github.com/3BMLabs/building.py",
    long_description=read('README.md'),
    install_requires=[
    ],
)