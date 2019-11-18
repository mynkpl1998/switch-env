from setuptools import setup

setup(name='switch',
    version='0.0.1',
    description='Switch - A multi-agent environement',
    py_modules=['switch', 'common', 'constants', 'parser'],
    package_dir={'':'src'},
    author='Mayank Kumar Pal',
    author_email='mayank15147@iiitd.ac.in',
    python_requires='>=3.6.*',
    project_urls={
        'Source Code': 'https://github.com/mynkpl1998/switch-env'})

