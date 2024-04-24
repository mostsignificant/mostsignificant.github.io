---
layout: post
title: "Empower New Python Projects with GitHub: Building and Sharing Your First Library"
date: 2023-06-13 23:45:10 +0200
categories: Python
comments: true
published: false
excerpt: |
  You wrote a handy Python script and now you want to share it with the world. Use GitHub and GitHub Actions to lift
  your functionality into a library, create pipelines for bundling, linting, testing, and releasing your code to the
  Open Source world.
image_url: /assets/images/unsplash/edgar-chaparro-d9UQsgHL2Ug-unsplash.jpg
image_description: |
  Photo by [Edgar Chaparro](https://unsplash.com/@echaparro?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
  on [Unsplash](https://unsplash.com/photos/d9UQsgHL2Ug?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
---

## The Goal

The following basic steps should be

- Building
- Linting
- Testing
- Releasing

## The Example Code

For this example, I prepared a simple script that provides methods for dumping files into a SQL database. The script
uses the pandas Dataframe functionality to write to the database. The library will be called **sqldump** and the according
script is already called `sqldump.py`.

## Setting Up A Python Library

This setup assumes, that the code is already in an according directory called `/sqldump/`. This will be the root folder
the library. Before starting to setup the library, we need to install the according command line tools to support our
undertaking:

```sh
pip install -U pip setuptools
```

Next, we need to create a `setup.py` file. This file contains all relevant library information.

```python
from setuptools import setup
from sqldump import __version__

setup(
    name='sqldump',
    version=__version__,

    url='https://github.com/mostsignificant/sqldump',
    author='Christian Göhring',
    author_email='mostsig@gmail.com',

    py_modules=['sqldump'],
)
```

The version information is already included in the `sqldump.py` file:

```python
__version__ = '0.0.1'
```

Afterwards we can confirm that everything is working correctly by installing this first version of the sqldump library:

```sh
pip install -e .
```

## Pushing Your Code To A GitHub Repository

A new GitHub account - if not existing - can be created with [a few clicks](https://github.com/signup). With the new
account, we create a [new repository](https://github.com/new) where the library will reside. We name the repository
**sqldump** according to the name of our library. A short description is an absolute minimum of documentation - even if
GitHub just marks it as _optional_. We select the _public_ option for the the repository to make the code available to
anyone, but do not add any other of the initialization options for the repository.

To put the local code under source control - if it is not already - we initialize a new local git repository:

```sh
cd sqldump/
git init .
```

Don't forget to add a proper `.gitignore` file so not every build artifact and config file lands in the repository. A
good example for Python development can found [here](https://github.com/github/gitignore/blob/main/Python.gitignore).
When done, let's commit all local changes:

```sh
git add .
git commit -m "initial commit"
```

After having committed the local files, we can add our new GitHub repository as origin and push it to the remote `main`
branch.

```sh
git remote add origin https://github.com/mostsignificant/sqldump.git
git branch -M main
git push -u origin main
```

The result can be checked on GitHub - the new repository should now contain all the files from the library.

## Enabling GitHub Actions

For using GitHub Actions, we need a so-called workflow definition. This definition must be put inside a YAML file, which
needs to placed inside a `.github/workflows` folder. Within this folder, we will name the file `package.yml`. Its
contents need to look like this for the start:

```yml
name: Build

on:
  push:
    branches: ["main"]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v3
        with:
          python-version: "3.x"
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install build
      - name: Build package
        run: python -m build
```

## Building

## Linting

For checking our script for errors and warnings, we will be using a so-called linter. A linter is a static analysis tool
which helps finding code that is buggy or that is potentially buggy. It also checks for stylistic issues or best
practice violations within the code.

For Python there exist several linters, for example:

- [Pylint](https://pypi.org/project/pylint/)
- [Flake8](https://pypi.org/project/flake8/)
- [Pyflakes](https://pypi.org/project/pyflakes/)
- [Pychecker](https://pypi.org/project/PyChecker/)
- [autopep8](https://pypi.org/project/autopep8/)

There is a well-written comparison of the first three of these linters in
[this blog article](https://dsstream.com/improve-your-python-code-quality/). Overall, Pylint shows the most features and
checks and is well-accepted within the community - so we will use this solution for our library.

We start by adding a new GitHub step to our build pipeline.

```yml
# ...
jobs:
  build:
    # ...
    steps:
      #...
      - name: Linting
        run: |
          pip install pylint
          pylint *.py
```

## Testing

Pytest is the widest spread library for testing Python code. We will use this for our build process, too.

The setup for our GitHub Action is super-simple. We will add a new step called _Testing_. Within this step, we install
`pytest` and then just call it via the same-named command `pytest`. Personally, I prefer to include the installation of
this tool in the same step as calling it. This has the advantage that the CI/CD configuration file is more modular.
Something regarding testing has to be fixed n the pipeline? No need to hop through several steps in the file. It could
increase the build time insignificantly because of a separate installation step.

```yml
# ...
jobs:
  build:
    # ...
    steps:
      #...
      - name: Testing
        run: |
          pip install pytest
          pytest
```

## Publishing

Finally, we want to publish our library to a build repository.

## Bonus

There is a lot more that can be done for a more complete CI/CD pipeline to leverage the full power of automation. Here
are some additional ideas that can be implemented:

- Generation and publishing of documentation (for example via
  [readthedocs](https://docs.readthedocs.io/en/stable/tutorial/index.html))
- Integration testing, in our example library via a real database and calling the tool via CLI
- Usage of more than just one linter for linting
