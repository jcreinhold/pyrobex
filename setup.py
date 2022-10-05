#!/usr/bin/env python

"""The setup script."""

from glob import glob
from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = [
    "nibabel",
    "numpy",
]

setup_requirements = []

test_requirements = [
    "tox",
    "pytest>=3",
]

robex_files = glob("pyrobex/ROBEX/**/*", recursive=True)
robex_dist = [file.replace("pyrobex/", "") for file in robex_files]
package_data = {"pyrobex": robex_dist}

setup(
    author="Jacob Reinhold",
    author_email="jcreinhold@gmail.com",
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    description="python bindings for ROBEX brain extraction",
    entry_points={"console_scripts": ["robex=pyrobex.cli:main",],},
    install_requires=requirements,
    license="BSD license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    package_data=package_data,
    keywords="robex, brain extraction, mri",
    name="pyrobex",
    packages=find_packages(include=["pyrobex", "pyrobex.*"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/jcreinhold/pyrobex",
    version="0.4.3",
    zip_safe=False,
)
