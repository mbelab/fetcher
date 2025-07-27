"""
Shell API for Python.
"""


# ----------------------------------------------------------------------------------------------------
# imports

import subprocess


# ----------------------------------------------------------------------------------------------------
# functions

def shell(input: str, directory=None, print_stdout=False, return_stderr=False):
    """Execute input in shell and return/print output as string."""

    # print input
    if print_stdout:
        if directory is not None:
            print("$ cd " + str(directory))
        print("$ " + input)

    # call shell using subprocess
    proc = subprocess.run(input, cwd=directory, capture_output=True, shell=True, check=True, text=True)

    # print output
    if print_stdout:
        print(proc.stdout)
        print("")

    # return output
    if return_stderr:
        return (proc.stdout, proc.stderr)
    else:
        return proc.stdout


def git(command: str, arguments: str = "", directory=None, print_stdout=False, return_stderr=False):
    """Execute git command with given arguments and return/print output as string."""

    input = "git" + " " + command + " " + arguments
    stdx = shell(input=input, directory=directory, print_stdout=print_stdout, return_stderr=return_stderr)

    return stdx
