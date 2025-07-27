"""
File utility functions.
"""


# ----------------------------------------------------------------------------------------------------
# imports

import os
import pathlib
import shutil
import json
import yaml

from fetcher.lib.defs import INDENT, ENCODING, NEWLINE


# ----------------------------------------------------------------------------------------------------
# functions

def mkdir(dir_path: str):
    """Make directory."""

    # make dir
    path_obj = pathlib.Path(dir_path)
    path_obj.mkdir(parents=True, exist_ok=True)


def prep_dir(file_path: str) -> str:
    """Prepare directory."""

    # prepare dirs for file path
    dir_path = os.path.dirname(file_path)
    mkdir(dir_path=dir_path)

    return file_path


def cp(src: str, dst: str):
    """Copy source to destination."""

    # copy
    if pathlib.Path(src).is_dir():
        shutil.copytree(src=src, dst=dst, copy_function=shutil.copy, dirs_exist_ok=True)
    else:
        prep_dir(file_path=dst)
        shutil.copy(src=src, dst=dst, follow_symlinks=False)

    return dst


def rm(path: str):
    """Remove path."""

    # remove
    path_obj = pathlib.Path(path)

    if path_obj.is_dir():
        shutil.rmtree(path=path, ignore_errors=True)
    else:
        path_obj.unlink(missing_ok=True)

    return path


def read_text(file_path: str) -> str:
    """Read text from ASCII/UTF-8 file."""

    # read text and return
    file = pathlib.Path(file_path)
    text = file.read_text(encoding=ENCODING)

    return text


def write_text(file_path: str, text: str):
    """Write text to ASCII/UTF-8 file."""

    # write text
    file = pathlib.Path(prep_dir(file_path=file_path))
    file.write_text(text, encoding=ENCODING, newline=NEWLINE)


def read_json(file_path: str):
    """Read data from json file."""

    # read data and return
    text = read_text(file_path=file_path)
    data = json.loads(text)

    return data


def write_json(file_path: str, data):
    """Write data to json file."""

    # write data
    text = json.dumps(data, indent=INDENT)
    write_text(file_path=file_path, text=text)


def read_yaml(file_path: str):
    """Read data from yaml file."""

    # read data and return
    text = read_text(file_path=file_path)
    data = yaml.safe_load(text)

    return data


def write_yaml(file_path: str, data):
    """Write data to yaml file."""

    # write data
    text = yaml.safe_dump(data, indent=INDENT, sort_keys=False)
    write_text(file_path=file_path, text=text)
