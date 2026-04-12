#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="pancharts",
    version="0.1.3",
    author="Wang Peng",
    author_email="wangpeng_621@163.com",
    description="A Python library for generating ECharts visualizations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wisherg/pancharts",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "pancharts": ["templates/*.html", "datasets/*.json"]
    },
    install_requires=[
        "pandas>=1.0.0",
        "jinja2>=2.11.0",
        "openai>=1.0.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)
