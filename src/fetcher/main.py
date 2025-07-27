#!/usr/bin/env python


"""
Fetcher

Python tool to fetch and manage resource files.

Author: mbelab - Michael Berghammer
"""


# ----------------------------------------------------------------------------------------------------
# imports

import pathlib
import argparse

from fetcher.lib.defs import ApplicationError
from fetcher.lib.shell import git
from fetcher.lib.misc import get_user, gen_timestamp
from fetcher.lib.file import mkdir, cp, rm, write_text, write_yaml, write_json, read_yaml, read_json
from fetcher.lib.http import http_get


# ----------------------------------------------------------------------------------------------------
# defines

YAML = "yaml"
JSON = "json"

META = "meta"
SETTINGS = "settings"
RESOURCES = "resources"
LOCAL = "local"
REPOSITORIES = "repositories"


# ----------------------------------------------------------------------------------------------------
# Resource class

class Resource:
    """Resource class."""

    FILE_TYPE = "file"
    GIT_TYPE = "git"
    HTTP_TYPE = "http"

    def __init__(self, entry: dict = {}) -> None:
        """Init resource."""

        self.active = False
        self.type = None
        self.dst = ""
        self.src = ""
        self.repository = None
        self.authorization = None

        if len(entry) > 0:
            self.set(entry=entry)

    def set(self, entry: dict) -> None:
        """Set resource data."""

        self.active = entry["active"]
        self.type = entry["type"]
        self.dst = entry["dst"]
        self.src = entry["src"]
        self.repository = entry["repository"]
        self.authorization = entry["authorization"]

    def get(self) -> dict:
        """Get resource data."""

        entry = {
            "active": self.active,
            "type": self.type,
            "dst": self.dst,
            "src": self.src,
            "repository": self.repository,
            "authorization": self.authorization,
        }

        return entry

    def fetch(self, local: str, repositories: str):
        """Fetch resource."""

        # fetch only if active
        if self.active:
            dst = local + self.dst

            # handle different types
            if self.type == Resource.FILE_TYPE:
                # copy file/directory
                cp(src=self.src, dst=dst)

            elif self.type == Resource.GIT_TYPE:
                # get repository name and path
                _, repository_name = self.repository.rsplit(sep="/", maxsplit=1)
                repository_name = repository_name.removesuffix(".git")
                repository_path = repositories + repository_name + "/"

                # clone repository if not existing
                if not pathlib.Path(repository_path).is_dir():
                    rm(path=repository_path)
                    git(command="clone", arguments=self.repository, directory=repositories)

                # update repository and possibly existing submodules
                git(command="reset", arguments="--hard", directory=repository_path)
                git(command="pull", arguments="--prune", directory=repository_path)
                git(command="submodule update", arguments="--init --recursive", directory=repository_path)

                # copy file/directory only if defined
                if self.src != "" and self.dst != "":
                    src = repository_path + self.src
                    cp(src=src, dst=dst)

            elif self.type == Resource.HTTP_TYPE:
                http_text = http_get(url=self.src, authorization=self.authorization)
                write_text(file_path=dst, text=http_text)

            else:
                err_msg = f"Resource type {self.type} is not supported."
                raise ApplicationError(err_msg)


# ----------------------------------------------------------------------------------------------------
# helper functions

def __store_resources_file(resources_file: str, resources: dict):
    """Store resources in file."""

    # handle file ending and store
    if resources_file.endswith(YAML):
        write_yaml(file_path=resources_file, data=resources)
    elif resources_file.endswith(JSON):
        write_json(file_path=resources_file, data=resources)
    else:
        print("File ending of resources file is not supported.")
        print("Use " + YAML + " or " + JSON + ".")


def __load_resources_file(resources_file: str) -> dict:
    """Load resources from file."""

    # handle file ending and load
    if resources_file.endswith(YAML):
        resources = read_yaml(file_path=resources_file)
    elif resources_file.endswith(JSON):
        resources = read_json(file_path=resources_file)
    else:
        print("File ending of resources file is not supported.")
        print("Use " + YAML + " or " + JSON + ".")

    # check toplevel dict keys and return
    if not META in resources:
        err_msg = f"Can not find toplevel dictionary key {META} in {resources_file}."
        raise ApplicationError(err_msg)
    if not SETTINGS in resources:
        err_msg = f"Can not find toplevel dictionary key {SETTINGS} in {resources_file}."
        raise ApplicationError(err_msg)
    if not RESOURCES in resources:
        err_msg = f"Can not find toplevel dictionary key {RESOURCES} in {resources_file}."
        raise ApplicationError(err_msg)

    return resources


def gen_resources_file(resources_file: str):
    """Generate new resources file."""

    # init resources and print user message
    resources = dict()
    print("Generate new resources file...")

    # add meta
    resources[META] = dict()
    resources[META]["info"] = "Fetcher resources file."
    resources[META]["date"] = gen_timestamp()
    resources[META]["user"] = get_user()
    resources[META]["note"] = ""

    # add settings
    resources[SETTINGS] = dict()
    resources[SETTINGS][LOCAL] = "./local/"  # default path to local resources
    resources[SETTINGS][REPOSITORIES] = "./local/repositories/"  # default path to local repositories

    # add resources with inactive example entries
    resources[RESOURCES] = list()

    entry = Resource()  # file/directory example
    entry.type = Resource.FILE_TYPE
    entry.dst = "local_file.txt"
    entry.src = "file_path/remote_file.txt"
    resources[RESOURCES].append(entry.get())

    entry = Resource()  # git repository example
    entry.type = Resource.GIT_TYPE
    entry.dst = "local_file.txt"
    entry.src = "file_path_in_repository/remote_file.txt"
    entry.repository = "ssh://git@server/project/repository.git"
    resources[RESOURCES].append(entry.get())

    entry = Resource()  # http example
    entry.type = Resource.HTTP_TYPE
    entry.dst = "local_file.txt"
    entry.src = "url_to_file"
    resources[RESOURCES].append(entry.get())

    # store resources
    __store_resources_file(resources_file=resources_file, resources=resources)


def clean_resources(resources_file: str):
    """Remove fetched resources."""

    # load resources and print user message
    resources = __load_resources_file(resources_file=resources_file)
    print("Remove fetched resources...")

    # remove repositories at first and then local
    local = resources[SETTINGS][LOCAL]
    repositories = resources[SETTINGS][REPOSITORIES]

    rm(path=repositories)
    rm(path=local)


def fetch(resources_file: str):
    """Fetch resources."""

    # load resources and print user message
    resources = __load_resources_file(resources_file=resources_file)
    print("Fetch resources...")

    # get paths from settings and prepare directories if necessary
    local = resources[SETTINGS][LOCAL]
    repositories = resources[SETTINGS][REPOSITORIES]

    if not local.endswith("/"):
        local = local + "/"
    if not repositories.endswith("/"):
        repositories = repositories + "/"

    mkdir(dir_path=local)
    mkdir(dir_path=repositories)

    # iterate over resources and fetch
    num_entries = len(resources[RESOURCES])
    entry_index = 1

    for entry in resources[RESOURCES]:
        print("Process " + str(entry_index) + "/" + str(num_entries) + "...")
        entry_index += 1

        resource = Resource(entry=entry)
        resource.fetch(local=local, repositories=repositories)


# ----------------------------------------------------------------------------------------------------
# core function

def fetcher(resources_file: str, generate=False, clean=False):
    """Fetcher."""

    # check and print resources_file
    resources_file_exists = pathlib.Path(resources_file).is_file()
    print("Resources file: " + resources_file)

    # handle input options
    if generate and clean:
        print("Can not generate new resources file and remove fetched resources in one step.")
        print("Use only one option per call, --generate or --clean.")
        print("Abort.")

    elif generate:
        if resources_file_exists:
            print("Resources file already exists.")
            user_input = input("Do you want to overwrite existing with new file? [y/N] ")

            if user_input != "" and user_input in ["y", "Y", "yes", "YES"]:
                gen_resources_file(resources_file=resources_file)
                print("Done.")
            else:
                print("Abort.")
        else:
            gen_resources_file(resources_file=resources_file)
            print("Done.")

    elif clean:
        if not resources_file_exists:
            print("Resources file does not exist.")
            print("Abort.")
        else:
            clean_resources(resources_file=resources_file)
            print("Done.")

    else:  # fetch
        if not resources_file_exists:
            print("Resources file does not exist.")
            print("Abort.")
        else:
            fetch(resources_file=resources_file)
            print("Done.")

    # finished
    return


# ----------------------------------------------------------------------------------------------------
# runner

def main():
    # program info
    description = "Fetch and manage resource files."
    epilog = "(c) mbelab - Michael Berghammer"

    # init parser for command line usage
    parser = argparse.ArgumentParser()
    parser.description = description
    parser.epilog = epilog

    # define arguments
    parser.add_argument("RESOURCES", help="Resources file")
    parser.add_argument("-g", "--generate", action="store_true", help="Generate new resources file")
    parser.add_argument("-c", "--clean", action="store_true", help="Remove fetched resources")

    # parse arguments and call main function with command line arguments
    args = parser.parse_args()
    fetcher(resources_file=args.RESOURCES, generate=args.generate, clean=args.clean)


if __name__ == '__main__':
    main()
