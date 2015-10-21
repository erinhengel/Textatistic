#!/user/bin/env python

from setuptools import setup

setup(
    name='textatistic',
    version='0.1',
    description='Calculate readability scores (Flesch Reading Ease, etc.).',
    author='Erin Hengel',
    url='http://www.erinhengel.com/software/textatistic/',
    packages = ['textatistic'],
    install_requires=['pyhyphen>=2.0.5'],
    package_data={'textatistic': ['abbreviations.txt', 'dale_chall.txt'], '': ['README.rst', 'LICENSE']},
    package_dir={'textatistic': 'textatistic'},
    include_package_data=True,
    author_email='erin.hengel@gmail.com',
    license='Apache 2.0',
    zip_safe=False,
    classifiers=(
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4'
    ),
)
