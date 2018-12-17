from datetime import datetime
from os import path
from typing import Union, Dict

import exifread


def _parse_date(input_val: str) -> Union[str, datetime]:
    """
    Try to parse the input string. If it is a parsable exif date, return a datetime object, otherwise None
    :param input_val: any string. If it is of the form yyyy:mm:dd HH:MM:SS, return a date
    """
    try:
        return datetime.strptime(str(input_val), '%Y:%m:%d %H:%M:%S')
    except ValueError:
        return input_val


def _exifread(filename: str) -> Dict[str, exifread.IfdTag]:
    """Wrapper for exifread.process_file"""
    with open(filename, 'rb') as f:
        return exifread.process_file(f, details=False)


def read_meta_data(filename: str) -> Dict[str, object]:
    """
    Extract EXIF meta-data from file as a dictionary. Add additional keys.

    :param filename: File with EXIF data to read
    :return: Dictionary with EXIF Key to exif values
    """
    props = _exifread(filename)
    # props is a dictionary with keys of the form "OptionGroup KeyName". Get rid of the OptionGroup part:
    res = {
        k.split(' ', 1)[-1]: _parse_date(v.values)
        for k, v in props.items()
    }
    res['full_file_name'] = filename
    pathname, basename = path.split(filename)
    res['file_name'] = basename
    res['path'] = pathname
    return res