#!/usr/bin/env python3

from setuptools import setup, find_packages

requirements = ['kaitaistruct']

from pathlib import Path
thisDir=Path(__file__).parent
formatsPath=thisDir / "kaitai"

setup(
    name='phasortoolbox',
    version='0.3',
    description='Synchrophasor Protocol parser and tools ',
    author='Xingsi',
    url="https://github.com/sonusz/PhasorToolBox",
    python_requires='>=3.5',
    install_requires=requirements,
    packages=find_packages(),
    kaitai={
        "formatsRepo":{},
        "formats":{},
        "search":True,
        "outputDir": thisDir / "phasortoolbox" / "parser",
        "inputDir": formatsPath
    },
    dependency_links = ["git+https://github.com/KOLANICH/kaitaiStructCompile.py.git"]
    )