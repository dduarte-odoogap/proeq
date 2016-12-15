#!/usr/bin/env python
"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='bashwrap',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='1.2.0',

    description='Bash Script Wrapper',
    long_description="""
    This Project Intends to Provide a set of tools for wrapping Bash Scripts
    """,

    # The project's main homepage.
    url='https://github.com/odoogap/bashwrap',

    # Author details
    author='Diogo Duarte',
    author_email='dduarte@odoogap.com',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Topic :: Software Development :: Odoo Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',

    ],

    # What does your project relate to?
    keywords='sample setuptools development',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['docs', 'tests']),
    include_package_data=True,
    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['paramiko', 'click', 'pyyaml'],
    test_suite='nose.collector',
    tests_require=['nose', 'nose-cover3'],
    entry_points={
        'console_scripts': ['proeq=proeq.cmd:cli'],
    },
)