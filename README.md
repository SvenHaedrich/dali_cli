# DALI cli

Command line interface to control a DALI system.

DALI is the digital addressable lighting interface as described [here](https://www.dali-alliance.org).

## Install from github

    git clone git@github.com:SvenHaedrich/dali_cli.git
    cd dali_cli
    python3 -m pip install --upgrade pip setuptools
    python3 -m build
    python3 -m pip install --editable .

## Building a Distribution

The `dali` command is distributed as a python package. [Setuptools](https://setuptools.pypa.io) is used to create the package. To build a new package, execute the following steps:

Install the latest version of `setuptools` using [pip](https://pypi.org/project/pip/)

    pip install --upgrade setuptools

Now you can build the distribution package

    cd dali_cli
    python -m build

Probably, you want to use the dali package in development mode. Here's how to do it:

    cd dali_cli
    pip install --editable .

