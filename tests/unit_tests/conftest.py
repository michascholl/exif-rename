import pytest


class ExifValue(object):
    def __init__(self, values):
        self.values = values


@pytest.fixture(autouse=True)
def no_exifread(monkeypatch):
    monkeypatch.setattr("exif_rename.parser._exifread", lambda file_, details=True: {
        'EXIF DateTime': ExifValue('2018:01:02 12:13:14'),
        'Instrument baz': ExifValue('bar'),
    })
