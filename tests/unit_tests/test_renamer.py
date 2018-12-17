from datetime import datetime

import pytest

from exif_rename.renamer import new_file_name


@pytest.fixture(scope='function')
def exif_props():
    return {
        'DateTime': datetime(2000, 1, 2, 12, 13, 14),
        'Model': 'MyCamera',
        'path': 'foo',
        'file_name': 'bar.jpg',
    }


@pytest.mark.parametrize('format_spec, expect', [
    ('baz', 'baz'),
    ('{DateTime:%Y-%m-%d_%H%M%S}', '2000-01-02_121314'),
])
def test_new_file_name(exif_props, format_spec, expect):
    res = new_file_name(format_spec, exif_props)
    assert res == expect


def test_new_file_name__missing_key(exif_props):
    with pytest.raises(KeyError) as exc:
        new_file_name('{missing}', exif_props)
    exc.match('Wrong format string')


def test_rename_file():
    pass
