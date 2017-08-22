import os
from datetime import date
from unittest.mock import MagicMock, call

import pytest
import imagesize

from kaleidoscope import renderer, generator
from kaleidoscope.model import Album, Gallery, Photo
from kaleidoscope.generator import generate, DefaultListener


def test_generate_gallery_index(tmpdir, disable_resize):
    """Generator should generate gallery index file."""
    gallery = Gallery("Testing Gallery", "The Tester", [])
    generate(gallery, str(tmpdir))
    assert tmpdir.join("index.html").check()


def test_gallery_index_context(tmpdir, monkeypatch, disable_resize):
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


def test_album_index_generated(tmpdir, gallery_with_one_photo, disable_resize):
    """Generator should create album index file."""
    generate(gallery_with_one_photo, str(tmpdir))
    assert tmpdir.join("album", "index.html").exists()


def test_album_index_context(tmpdir, monkeypatch, disable_resize):
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
    assert photo.thumb.url == "thumb/photo.jpg"
    assert photo.thumb.size <= (300, 200)
    assert photo.large.url == "large/photo.jpg"
    assert photo.large.size <= (1500, 1000)


def test_copy_assets(tmpdir, disable_resize):
    """Generator should copy assets directory into output."""
    gallery = Gallery("", "", [])
    generate(gallery, str(tmpdir))
    assert tmpdir.join("assets", "kaleidoscope.js").exists()
    assert tmpdir.join("assets", "kaleidoscope.css").exists()


def test_assets_directory_cleaned(tmpdir, disable_resize):
    """Generator should clean up existing assets directory."""
    extra_file = tmpdir.join("assets", "existing-file.txt")
    extra_file.ensure()
    generate(Gallery("", "", []), str(tmpdir))
    assert not extra_file.exists()


def test_generator_reporting_events(gallery_with_three_photos, tmpdir,
                                    disable_resize):
    """Generator should report important events using provided reporter."""
    listener = MagicMock(spec=DefaultListener)
    generate(gallery_with_three_photos, tmpdir, listener)

    album = gallery_with_three_photos.albums[0]
    assert listener.starting_album.call_args == call(album, 3)
    assert listener.finishing_album.called
    assert listener.resizing_photo.call_count == 3


def test_counting_photos_to_resize(
        gallery_with_three_photos, tmpdir, disable_resize):
    """Listener should receive count of photos that would be really resized."""
    # Let's make 1.jpg already resized => 2 photos would remain
    tmpdir.join("album", "large", "f1.jpg").ensure()
    tmpdir.join("album", "thumb", "f1.jpg").ensure()

    listener = MagicMock(spec=DefaultListener)
    generate(gallery_with_three_photos, tmpdir, listener)

    album = gallery_with_three_photos.albums[0]
    assert listener.starting_album.call_args == call(album, 2)
    assert listener.resizing_photo.call_count == 2


@pytest.fixture
def gallery_with_one_photo():
    photo_path = os.path.join(os.path.dirname(__file__), 'data', 'photo.jpg')
    photo = Photo("photo.jpg", "", "", photo_path)
    album = Album("album", "The Album", date(2017, 6, 24), [photo])
    return Gallery("Testin Gallery", "The Tester", [album])


@pytest.fixture
def gallery_with_three_photos():
    photo_path = os.path.join(os.path.dirname(__file__), 'data', 'photo.jpg')
    photos = [Photo("f%d.jpg" % (i,), "", "", photo_path) for i in range(3)]
    album = Album("album", "The Album", date(2017, 6, 24), photos)
    return Gallery("Testing Gallery", "The Tester", [album])


@pytest.fixture
def disable_resize(monkeypatch):
    """Replace image resize with dummy function and provide constant size."""
    monkeypatch.setattr(generator, 'resize', MagicMock())
    monkeypatch.setattr(imagesize, 'get', MagicMock(return_value=(42, 42)))
