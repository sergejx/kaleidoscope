from datetime import datetime
from pathlib import Path
from shutil import copy
from tempfile import TemporaryDirectory
from unittest import TestCase, mock

from kaleidoscope import gallery
from kaleidoscope.config import GalleryConfigParser


class TestInit(TestCase):
    """Test initialization of gallery or album."""
    def test_init_gallery(self):
        """generate_gallery_ini function should generate valid configuration."""
        with TestingGallery(with_gallery_conf=False) as gallery_path:
            gallery.generate_gallery_ini(gallery_path)
            self.assert_valid_configuration(gallery_path / 'gallery.ini',
                                            {'gallery': ['title', 'author']})

    def test_init_album(self):
        """generate_album_ini function should generate configuration with all photos."""
        with TestingGallery(with_album_conf=False) as gallery_path:
            album_path = gallery_path / 'testing-album'
            gallery.generate_album_ini(album_path)
            self.assert_valid_configuration(album_path / 'album.ini', {
                'album': ['title', 'date'],
                'photos': TestingGallery.PHOTOS
            })

    def assert_valid_configuration(self, path, sections):
        """Check if configuration file exists and has specified sections and options."""
        self.assertTrue(path.exists())
        config = GalleryConfigParser()
        config.read(str(path))
        for section, options in sections.items():
            self.assertTrue(config.has_section(section))
            for option in options:
                self.assertTrue(config.has_option(section, option))


class TestAlbum(TestCase):
    maxDiff = None

    @mock.patch('kaleidoscope.photo.Photo.__init__')
    def test_read_album(self, mock_photo_init):
        mock_photo_init.return_value = None
        gallery_mock = mock.MagicMock()

        with TestingGallery() as gallery_path:
            gallery_mock.output = gallery_path / 'output'
            album_path = gallery_path / TestingGallery.ALBUM_NAME
            album_output = gallery_path / 'output' / TestingGallery.ALBUM_NAME

            album = gallery.Album(gallery_mock, album_path)

            self.assertEqual(album.name, TestingGallery.ALBUM_NAME)
            self.assertEqual(album.path, album_path)
            self.assertEqual(album.output, album_output)
            self.assertEqual(album.title, "Testing Album")
            self.assertEqual(album.date, datetime(2017, 5, 15, 0, 0))
            self.assertEqual(len(album.photos), 4)
            self.assertListEqual(mock_photo_init.call_args_list, [
                mock.call(album_path / 'Photo1.jpg', album_output, ''),
                mock.call(album_path / 'Photo2.jpg', album_output, 'Caption'),
                mock.call(album_path / 'Photo3.jpg', album_output, 'Long caption'),
                mock.call(album_path / 'Photo4.jpg', album_output, 'Long caption| with hidden part')
            ])


class TestingGallery:
    """
    Context manager creating and cleaning up temporary testing gallery.
    Returns a Path of the gallery.
    """
    DATA_PATH = Path(__file__).parent / 'data'
    PHOTOS = ['Photo1.jpg', 'Photo2.jpg', 'Photo3.jpg', 'Photo4.jpg']
    ALBUM_NAME = 'testing-album'

    def __init__(self, with_gallery_conf=True, with_album_conf=True):
        self.tempdir = TemporaryDirectory()
        self.tempdir_path = Path(self.tempdir.name)
        if with_gallery_conf:
            copy(str(self.DATA_PATH / 'gallery.ini'), self.tempdir.name)
        self.create_album(self.ALBUM_NAME, with_album_conf)

    def create_album(self, album_name, with_album_conf):
        album_path = self.tempdir_path / album_name
        album_path.mkdir()
        if with_album_conf:
            copy(str(self.DATA_PATH / 'album.ini'), str(album_path))
        for photo in self.PHOTOS:
            copy(str(self.DATA_PATH / 'photo.jpg'), str(album_path / photo))

    def __enter__(self) -> Path:
        return self.tempdir_path

    def __exit__(self, exc_type, exc_value, traceback):
        self.tempdir.cleanup()
