from setuptools import setup
from src.common import readFile

fileHandle = readFile("requirements.txt")
description = readFile("README.md").read()
install_requires = fileHandle.read().splitlines()

setup(name='switch',
    version='0.0.1',
    description='Switch - A multi-agent environement',
    long_description=description,
    long_description_content_type="text/markdown",
    py_modules=['switch', 'common', 'constants', 'mapParser', 'ui'],
    package_dir={'':'src'},
    author='Mayank Kumar Pal',
    install_requires=install_requires,
    author_email='mayank15147@iiitd.ac.in',
    python_requires='>=3.6.*',
    project_urls={
        'Source Code': 'https://github.com/mynkpl1998/switch-env'})

