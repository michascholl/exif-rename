from tempfile import NamedTemporaryFile
from datetime import datetime

import pytest

from exif_rename.parser import _parse_date, read_meta_data


@pytest.fixture
def tempfile():
    with NamedTemporaryFile() as tempfile:
        yield tempfile.name


@pytest.mark.parametrize('input', [
    'non-date', '2018-01-02 12:14:15'
])
def test_parse_date__no_date(input):
    res = _parse_date(input)
    assert res == input


@pytest.mark.parametrize('input', [
    '2018:01:02 12:14:15'])
def test_parse_date__valid_date(input):
    res = _parse_date(input)
    assert res == datetime.strptime(input, '%Y:%m:%d %H:%M:%S')


@pytest.mark.parametrize('attr', [
    'DateTime',
    'baz',
    # custom attributes:
    'file_name',
    'path',
    'full_file_name',
])
def test_read_meta_data__add_attributes(attr, tempfile):
    res = read_meta_data(tempfile)
    assert attr in res


def test_read_meta_data__convert_date(tempfile):
    res = read_meta_data(tempfile)
    assert isinstance(res['DateTime'], datetime)


