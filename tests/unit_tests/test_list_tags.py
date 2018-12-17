import pytest

from exif_rename.list_tags import get_common_samples
from os.path import join

@pytest.mark.parametrize('key, expect', [
    ('file_name', {'str: "a"', 'str: "b"'}),
    ('baz', {'str: "bar"'}),
    ('path', {'str: "{}"'.format(join(*'xy'))}),
])
def test_get_common_samples(key, expect):
    res = get_common_samples([join(*'xya'), join(*'xyb')])
    assert res[key] == expect


def test_get_common_samples__no_files():
    res = get_common_samples([])
    assert len(res) == 0


def test_get_common_samples__non_common_exif(monkeypatch):
    def mock_read_meta_data(filename):
        return {
            'common1': 'Foo' + filename,
            'common2': 'Bar',
            filename: 'Unique Value',
            filename + '_unique': filename,
        }

    monkeypatch.setattr('exif_rename.list_tags.read_meta_data', mock_read_meta_data)
    res = get_common_samples(['a', 'b'])
    assert set(res.keys()) == {'common1', 'common2'}
    assert res['common1'] == {'str: "Fooa"', 'str: "Foob"'}
    assert res['common2'] == {'str: "Bar"'}
