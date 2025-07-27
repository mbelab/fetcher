# fetcher

Python tool to fetch and manage resource files.

**Maintainer:** [Michael Berghammer](mailto:info@mbelab.de)

> **Note:** Files in subdirectories named *private* are not tracked by Git.

This tool can fetch (clone and update) files, defined in a human-readable file.  
Resources files can be in `yaml` or `json` format and can be edited with any text editors.

Currently there are several types of resources supported:

- `file` type: Local or remote files.
- `git` type: Files in (remote) git repositories.
- `http` type: File content, accessible via http.

For installation and usage see:

- [usage](#usage)
- [install](#install)

## usage

Get command line info:

    $ fetcher --help

    usage: fetcher [-h] [-g] [-c] RESOURCES

    Fetch and manage resource files.

    positional arguments:
    RESOURCES       Resources file

    options:
    -h, --help      show this help message and exit
    -g, --generate  Generate new resources file
    -c, --clean     Remove fetched resources

    (c) mbelab - Michael Berghammer

Generate template resources file:

    $ fetcher --generate resources.yaml

    Resources file: resources.yaml
    Generate new resources file...
    Done.

Update resources defined in resources file:

    $ fetcher resources.yaml

    Resources file: resources.yaml
    Fetch resources...
    Process 1/3...
    Process 2/3...
    Process 3/3...
    Done.

Cleanup resources defined in resources file:

    $ fetcher --clean resources.yaml

    Resources file: resources.yaml
    Remove fetched resources...
    Done.

## install

Install `fetcher`:

    $ pip install .

Install `fetcher` locally (virtual environment):

    $ python3 -m virtualenv .venv
    $ source .venv/bin/activate

    $ pip install .

Build `wheel` for e.g. deployment (locally):

    $ python3 -m virtualenv .venv
    $ source .venv/bin/activate

    $ pip install build
    $ python -m build

Install from `wheel`:

    $ pip install dist/*.whl

Prepare environment/shell for local development:

    $ python3 -m virtualenv .venv
    $ source .venv/bin/activate

    $ pip install -r requirements.txt
    $ export PYTHONPATH='./src'
