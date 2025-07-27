"""
Miscellaneous utility functions.
"""


# ----------------------------------------------------------------------------------------------------
# imports

import os
import datetime


# ----------------------------------------------------------------------------------------------------
# functions

def get_user() -> str:
    """Get currently logged in user."""

    # get user and return
    user = os.getlogin()

    return user


def gen_timestamp(no_time=False, no_colon=False) -> str:
    """Gen ISO 8601 timestamp (YYYY-MM-DDThh:mm:ss)."""

    # gen timestamp and return
    now = datetime.datetime.now()
    timestamp = now.isoformat(sep="T", timespec="seconds")

    # gen timestamp without time information
    if no_time:
        timestamp = timestamp[:10]

    # gen timestamp without colon for e.g. Windows file paths
    if no_colon:
        timestamp = timestamp.replace(":", "")

    return timestamp
