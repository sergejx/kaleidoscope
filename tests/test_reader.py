import os
import shutil
from datetime import datetime
import pytest

from kaleidoscope import reader


def test_read_gallery(testing_gallery):
    """Reader should properly read metadata of the gallery."""
    gallery = reader.read_gallery(str(testing_gallery))
    assert gallery.title == "Hello World"
    assert gallery.author == "Me"
    assert len(gallery.albums) == 1


def test_read_album(testing_gallery):
    album_dir = str(testing_gallery.join("testing-album"))
    album = reader.read_album(album_dir)
    assert album.name == "testing-album"
    assert album.title == "Testing Album"
    assert album.date == datetime(2017, 5, 15, 0, 0)


def test_read_photos(testing_gallery):
    album_dir = str(testing_gallery.join("testing-album"))
    album = reader.read_album(album_dir)
    expected_photos = [
        ("Photo1.jpg", "", ""),
        ("Photo2.jpg", "Caption", "Caption"),
        ("Photo3.jpg", "Long caption", "Long caption"),
        ("Photo4.jpg", "Long caption", "Long caption with hidden part")
    ]
    for photo, (name, short_caption, long_caption) in \
            zip(album.photos, expected_photos):
        assert photo.name == name
        assert photo.short_caption == short_caption
        assert photo.long_caption == long_caption
        assert photo.source_path == os.path.join(album_dir, name)


@pytest.fixture
def testing_gallery(tmpdir):
    data_path = os.path.join(os.path.dirname(__file__), 'data')
    photos = ['Photo1.jpg', 'Photo2.jpg', 'Photo3.jpg', 'Photo4.jpg']
    shutil.copy(os.path.join(data_path, 'gallery.ini'), str(tmpdir))
    album_path = tmpdir.join('testing-album')
    album_path.mkdir()
    shutil.copy(os.path.join(data_path, 'album.ini'), str(album_path))
    for photo in photos:
        shutil.copy(os.path.join(data_path, 'photo.jpg'),
                    str(album_path.join(photo)))
    return tmpdir
