# fetcher

Python tool to fetch and manage resource files.

**Maintainer:** [Michael Berghammer](mailto:info@mbelab.de)

> **Note:** Files in subdirectories named *private* are not tracked by Git.

## usage

Install `fetcher`:

    pip install .

Install `fetcher` locally (virtual environment):

    python3 -m virtualenv .venv
    source .venv/bin/activate

    pip install .

Build `wheel` for e.g. deployment (locally):

    python3 -m virtualenv .venv
    source .venv/bin/activate

    pip install build
    python -m build

Install from `wheel`:

    pip install dist/*.whl

Prepare environment/shell for local development:

    python3 -m virtualenv .venv
    source .venv/bin/activate

    pip install -r requirements.txt
    export PYTHONPATH='./src'
