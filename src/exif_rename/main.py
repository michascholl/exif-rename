from typing import List

import click

from exif_rename.renamer import new_file_name, rename_file
from exif_rename.parser import read_meta_data
from exif_rename.list_tags import list_common_tags


@click.command(name='exif_renamer')
@click.option('--verbose/--quiet', '-v/-q', default=False)
@click.option('--exists', default='keep', show_default=True, type=click.Choice(['keep', 'overwrite', 'error']))
@click.option('--noop', default=False, show_default=False)
@click.option('--list', default=False, is_flag=True, help='List the common tags')
@click.argument('template', type=str)
@click.argument('files', nargs=-1)
def main(template, files: List[str], verbose: bool, exists: str, noop: bool, list: bool) -> None:
    """
    Rename image files based on EXIF meta-information.

    Template is the new file name template using python format syntax. As variables
    """
    if list:
        list_common_tags([template] + files, 3)
        return
    for old_file in files:
        exif_vars = read_meta_data(old_file)
        new_file = new_file_name(template, exif_vars)
        if verbose:
            print('{} -> {}'.format(old_file, new_file))
        if not noop:
            rename_file(old_file, new_file, exists)


if __name__ == '__main__':
    main()
