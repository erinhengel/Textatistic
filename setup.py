#!/user/bin/env python

from setuptools import setup, find_packages

setup(
    name='textatistic',
    version='0.1',
    packages = find_packages(),
    scripts = ['textatistic.py'],
    install_requires = ['pyhyphen>=2.0.5'],
    package_data = {'': ['dale_chall.txt', 'abbreviations.txt', 'LICENSE']}
    description='Calculate readability scores (Flesch Reading Ease, etc.).',
    long_description=open('README.md').read(),
    author='Erin Hengel',
    author_email='erin.hengel@gmail.com',
    url='http://www.erinhengel.com/software/textatistic/',
    license='Apache 2.0',
    classifiers=(
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4'
    )
)