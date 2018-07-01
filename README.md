ToC:
- [Asset-Allocation](#asset-allocation)
    - [Introduction](#introduction)
- [Development](#development)
    - [Configuration](#configuration)
    - [Data Store](#data-store)
- [Tests](#tests)
- [Distribution](#distribution)
    - [Test Site](#test-site)
    - [Production Site](#production-site)

# Asset-Allocation
Asset Allocation implementation in Python

## Introduction 

The idea here is to encapsulate Asset Allocation logic into a separate component and make it available to other projects (GnuCash Portfolio, and Android apps).

This will include its own data storage.

Dependencies will include:
- price database, for calculation of current value
- transaction database for securities, for calculation of current value

# Development

Requirements are generated with _pipreqs_. Install requirements from requirements.txt.

## Configuration

On the first run, a config file will be created in the user's directory, based on the template in project's data directory.

## Data Store

Data storage is in a SQLite database, which allows for portability, easy queries and relatively easy editing.
The sample data file is in "data" folder.

# Tests

To lint the code, execute `pylint` from the project root directory.
To run tests, execute `pytest` from the project root directory.

# Distribution

## Test Site

```console
python setup.py sdist upload -r test
```

## Production Site

```console
python setup.py sdist upload -r pypi
```