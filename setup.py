#!/usr/bin/env python
import os
from pathlib import Path

from setuptools import find_packages, setup

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
requirements = """
crossplane==0.5.7
pydantic==1.8.2
loguru==0.5.3
prettytable==2.5.0
"""


setup(
    name="nginx-static-analysis",
    version="0.2.4",
    description="Parse Nginx configurations in a clear manner for debugging purposes",
    url="https://github.com/AlexanderGrooff/nginx-static-analysis",
    packages=find_packages(
        include=["nginx_analysis", "requirements/base.txt"], exclude=["tests"]
    ),
    author="Alexander Grooff",
    author_email="alexandergrooff@gmail.com",
    install_requires=requirements.split("\n"),
    entry_points={
        "console_scripts": [
            "nginx-static-analysis = nginx_analysis.main:main",
        ],
    },
    python_requires=">=3.7",
    long_description=long_description,
    long_description_content_type="text/markdown",
)
