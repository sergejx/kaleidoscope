import os
from datetime import date
from unittest.mock import MagicMock

import pytest
import imagesize

from kaleidoscope import renderer
from kaleidoscope.model import Album, Gallery, Photo
from kaleidoscope.generator import generate


def test_generate_gallery_index(tmpdir):
    """Generator should generate gallery index file."""
    gallery = Gallery("Testing Gallery", "The Tester", [])
    generate(gallery, str(tmpdir))
    assert tmpdir.join("index.html").check()


def test_gallery_index_context(tmpdir, monkeypatch):
    """Generator should provide the gallery object for index template."""
    render_mock = MagicMock()
    monkeypatch.setattr(renderer, 'render', render_mock)

    gallery = Gallery("Testing Gallery", "The Tester", [])
    generate(gallery, str(tmpdir))

    render_mock.assert_called_with(
        "gallery.html",
        str(tmpdir.join("index.html")),
        {'gallery': gallery, 'current_year': date.today().year}
    )


def test_album_index_generated(tmpdir, gallery_with_one_photo):
    """Generator should create album index file."""
    generate(gallery_with_one_photo, str(tmpdir))
    assert tmpdir.join("album", "index.html").exists()


def test_album_index_context(tmpdir, monkeypatch):
    """
    Generator should provide provide correct context to the album template.
    """
    render_mock = MagicMock()
    monkeypatch.setattr(renderer, 'render', render_mock)

    album = Album("album", "The Album", date(2017, 6, 24), [])
    gallery = Gallery("Testin Gallery", "The Tester", [album])
    generate(gallery, str(tmpdir))

    render_mock.assert_called_with(
        "album.html",
        str(tmpdir.join("album", "index.html")),
        {'album': album, 'gallery': gallery, 'current_year': date.today().year}
    )


def test_resize_thumbnail(tmpdir, gallery_with_one_photo):
    """Generator should create thumbnail file."""
    generate(gallery_with_one_photo, str(tmpdir))
    thumb_path = tmpdir.join("album", "thumb", "photo.jpg")
    assert thumb_path.exists()
    assert imagesize.get(str(thumb_path)) <= (300, 200)


def test_resize_large(tmpdir, gallery_with_one_photo):
    """Generator should create large resized file."""
    generate(gallery_with_one_photo, str(tmpdir))
    large_path = tmpdir.join("album", "large", "photo.jpg")
    assert large_path.exists()
    assert imagesize.get(str(large_path)) <= (1500, 1000)


def test_resize_existing(tmpdir, gallery_with_one_photo):
    """When resized image allready exists, do not resize it again."""
    thumb_path = tmpdir.join("album", "thumb", "photo.jpg")
    large_path = tmpdir.join("album", "large", "photo.jpg")
    thumb_path.ensure()
    large_path.ensure()
    original_thumb_mtime = thumb_path.mtime()
    original_large_mtime = large_path.mtime()

    generate(gallery_with_one_photo, str(tmpdir))
    assert thumb_path.mtime() == original_thumb_mtime
    assert large_path.mtime() == original_large_mtime


def test_resized_images_metadata(tmpdir, gallery_with_one_photo):
    """Generator should fill resized images metadata in the Photo."""
    generate(gallery_with_one_photo, str(tmpdir))
    photo = gallery_with_one_photo.albums[0].photos[0]
    assert photo.thumb.url == ("thumb/photo.jpg")
    assert photo.thumb.size <= (300, 200)
    assert photo.large.url == ("large/photo.jpg")
    assert photo.large.size <= (1500, 1000)


def test_copy_assets(tmpdir):
    """Generator should copy assets directory into output."""
    gallery = Gallery("", "", [])
    generate(gallery, str(tmpdir))
    assert tmpdir.join("assets", "kaleidoscope.js").exists()
    assert tmpdir.join("assets", "kaleidoscope.css").exists()
    assert tmpdir.join("assets", "vendor").exists()


def test_assets_directory_cleaned(tmpdir):
    """Generator should clean up existing assets directory."""
    extra_file = tmpdir.join("assets", "existing-file.txt")
    extra_file.ensure()
    generate(Gallery("", "", []), str(tmpdir))
    assert not extra_file.exists()


@pytest.fixture
def gallery_with_one_photo():
    photo_path = os.path.join(os.path.dirname(__file__), 'data', 'photo.jpg')
    photo = Photo("photo.jpg", "", "", photo_path)
    album = Album("album", "The Album", date(2017, 6, 24), [photo])
    return Gallery("Testin Gallery", "The Tester", [album])
