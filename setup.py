#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import setuptools
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()
setup(
    name="guolei-py3-hikvision",
    version="0.0.3",
    description="海康威视 API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/guolei19850528/guolei_py3_hikvision",
    author="guolei",
    author_email="174000902@qq.com",
    license="MIT",
    keywors=["海康威视", "hikvision"],
    packages=setuptools.find_packages('./'),
    install_requires=[
        "addict",
        "retrying",
        "pydantic",
        "guolei-py3-requests",
    ],
    python_requires='>=3.0',
    zip_safe=False
)
