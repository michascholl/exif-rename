"""
module responsible for renaming of files
"""
import os
import pathlib
from os import path
from typing import Dict


def new_file_name(format_spec: str, exif_props: Dict[str, object]) -> str:
    """Get the new file name based on the template and the old file name"""
    try:
        return format_spec.format(**exif_props)
    except KeyError:
        print('Possible missing format string. Valid formats are:\n{}'.format(
            '  '.join(exif_props.keys())
        ))
        raise KeyError('Wrong format string')


def rename_file(old_file: str, new_file: str, exists: str) -> None:
    """
    Rename old_file to new_file. If new_file exits already, either keep or overwrite the new file or bail out with a
    FileExistsError, depending of the setting in `exists` (one of overwrite, keep, error),

    """
    dir_name, _ = path.split(new_file)
    if path.exists(new_file):
        if exists == 'overwrite':
            os.unlink(new_file)
        elif exists == 'keep':
            print('{} -> {}. Target file exists. Do not overwrite.'.format(old_file, new_file))
            return
        elif exists == 'error':
            raise FileExistsError(new_file)
        else:
            raise ValueError('Unknown option "{}" for exists'.format(exists))

    if not path.exists(dir_name):
        pathlib.Path(dir_name).mkdir(parents=True, exist_ok=True)
    os.rename(old_file, new_file)