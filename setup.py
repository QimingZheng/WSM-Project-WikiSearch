import setuptools
from setuptools import find_packages
# from setuptools import Extension
# from setuptools.command.install import install
# from setuptools.command.develop import develop
# from setuptools.command.install_lib import install_lib
# from setuptools.command.build_ext import build_ext as build_ext_orig
from subprocess import check_call
from distutils.sysconfig import get_python_lib
import os
import platform
import pathlib
import atexit
import shutil

with open("README.md", "r") as fh:
    long_description = fh.read()

_packages = find_packages(where='./wikisearch', exclude=(), include=('*', ))
packages = ["wikisearch/" + pack for pack in _packages
            ] + ["wikisearch", "wikisearch/deps/wikiextractor"]

setuptools.setup(
    name="wikisearch",
    version="0.0.1",
    author="Qiming Zheng",
    author_email="qimingzheng96@gmail.com",
    description="A search engine for wikipedia",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/QimingZheng/wikipedia-search-engine",
    keywords=["Search Engine", "IR"],
    # packages=['wikisearch'],
    packages=
    packages,  # [find_packages(where='./wikisearch', exclude=(), include=('*',)),
    install_requires=[],
    python_requires='>=3.5',
    data_files=[("", ["LICENSE"])],
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    # cmdclass = {
    #     'install_lib': PostInstallCommand,
    # },
)