import yaml
from typing import Any
from datetime import datetime


def open_file(path: str, mode: str = "r") -> Any:
    """Read file
    
    :param path: path where the file resides
    :param mode: currently only handle `r`
    """

    if mode != "r":
        return NotImplementedError()
    
    file_name = path.split(".")
    file_ext = file_name[-1]

    if file_ext == "yaml":
        with open(path, mode) as file:
            return yaml.safe_load(file)
    else:
        with open(path, open) as file:
            return file.read()

def convert_to_strftime(dt: datetime):
    """Convert datetime data to strftime format"""
    
    return dt.strftime('%Y-%m-%dT%H:%M:%SZ')