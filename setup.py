#!/usr/bin/env python
import os

from setuptools import find_packages, setup

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


def get_requires_based_on_dist():
    return ["crossplane"]


setup(
    name="nginx-static-analysis",
    version="0.1.0",
    description="Parse Nginx configurations in a clear manner for debugging purposes",
    url="https://github.com/AlexanderGrooff/nginx-static-analysis",
    packages=find_packages(exclude=["tests", "tests.*"]),
    author="Alexander Grooff",
    author_email="alexandergrooff@gmail.com",
    install_requires=get_requires_based_on_dist(),
    entry_points={
        "console_scripts": [
            "nginx-static-analysis = nginx_analysis.main:main",
        ],
    },
)
