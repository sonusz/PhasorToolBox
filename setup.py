#!/usr/bin/env python3

from setuptools import setup, find_packages

requirements = ['kaitaistruct', 'uvloop']

setup(
    name='phasortoolbox',
    version='0.2',
    description='Synchrophasor Protocol parser and tools ',
    author='Xingsi',
    url="https://github.com/sonusz/PhasorToolBox",
    python_requires='>=3.5',
    install_requires=requirements,
    packages=find_packages(),
    )
