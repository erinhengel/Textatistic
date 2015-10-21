#!/user/bin/env python

from setuptools import setup, find_packages

setup(
    name='textatistic',
    version='0.001',
    packages = ['textatistic'],
    install_requires = ['pyhyphen>=2.0.5'],
    package_data = {'': ['LICENSE'], 'textatistic': ['dale_chall.txt', 'abbreviations.txt']},
    author='Erin Hengel',
    author_email='erin.hengel@gmail.com',
    description='Calculate readability scores (Flesch Reading Ease, etc.).',
    long_description=open('README.md').read(),
    url='http://www.erinhengel.com/software/textatistic/',
    license='Apache 2.0',
    classifiers=(
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4'
    )
)
