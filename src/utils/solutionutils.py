from os import getcwd
from pathlib import Path


def get_project_root() -> str:
    """
    Returns path of the project root
    Returns
    -------
    str
        path of the project root
    """
    return str(Path(getcwd().split('src')[0] + '/'))
