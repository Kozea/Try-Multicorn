#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2011 by Ronan Dunklau, Kozea
# This file is part of multicorn-demo, licensed under a 3-clause BSD license.

"""
A demo for multicorn
"""

from setuptools import setup, find_packages

options = dict(
    name="multicorn-demo",
    version="0.0.1",
    description="A showcase for multicorn",
    long_description=__doc__,
    author="Ronan Dunklau - Kozea",
    author_email="ronan.dunklau@kozea.fr",
    license="BSD",
    platforms="Any",
    packages=find_packages(),
    install_requires=["flask>=0.7", 'flask-sqlalchemy', 'csstyle'],
    classifiers=[
        "Development Status :: WIP",
        "Intended Audience :: Public",
        "License :: OSI Approved :: BSD License",
        "Operating System :: Linux",
        "Programming Language :: Python :: 2.7"])

setup(**options)
