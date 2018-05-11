#!/usr/bin/env python3

from setuptools import setup, find_packages

requirements = ['kaitaistruct']

setup(
    name='phasortoolbox',
    version='0.3',
    description='Synchrophasor Protocol parser and tools ',
    author='Xingsi',
    url="https://github.com/sonusz/PhasorToolBox",
    python_requires='>=3.5',
    install_requires=requirements,
    packages=find_packages(),
    )
