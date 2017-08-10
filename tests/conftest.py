import os
import shutil

import pytest


DATA_PATH = os.path.join(os.path.dirname(__file__), 'data')


@pytest.fixture
def testing_gallery(tmpdir):
    """Testing gallery with two albums:
    - testing-album
    - album-incomplete (without album metadata in album.ini)
    Both galleryes contain four photos: Photo{1..4}.jpg
    """
    shutil.copy(os.path.join(DATA_PATH, 'gallery.ini'), str(tmpdir))
    _create_album(tmpdir, 'testing-album', 'album.ini')
    _create_album(tmpdir, 'incomplete-album', 'album-incomplete.ini')
    return tmpdir


def _create_album(gallery_dir, album_name, ini_name):
    photos = ['Photo1.jpg', 'Photo2.jpg', 'Photo3.jpg', 'Photo4.jpg']
    album_path = gallery_dir.join(album_name)
    album_path.mkdir()
    shutil.copy(os.path.join(DATA_PATH, ini_name),
                str(album_path.join('album.ini')))
    for photo in photos:
        shutil.copy(os.path.join(DATA_PATH, 'photo.jpg'),
                    str(album_path.join(photo)))
