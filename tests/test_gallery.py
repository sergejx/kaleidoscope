import unittest
from configparser import ConfigParser
from datetime import date
from pathlib import Path
from shutil import copyfile
from tempfile import TemporaryDirectory

from kaleidoscope.gallery import GalleryConfigParser, Photo, \
    generate_gallery_ini, generate_album_ini


class TestGalleryConfigParser(unittest.TestCase):
    def test_lowercase_key(self):
        """Lowercase option key is left as is."""
        config = GalleryConfigParser()
        config.read_string("[album]\ntitle: Example\n")
        self.assertTrue(config.has_option('album', 'title'))

    def test_mixedcase_key(self):
        """Other keys are converted to lowercase."""
        config = GalleryConfigParser()
        config.read_string("[album]\nTitle: Example\n")
        self.assertTrue(config.has_option('album', 'title'))

    def test_filename_key(self):
        """Filename keys (with dot) are case sensitive."""
        config = GalleryConfigParser()
        config.read_string("[photos]\nDSC3000.JPG: UPPER\ndsc2000.jpg: lower\n")
        self.assertEqual(config.options('photos'),
                         ['DSC3000.JPG', 'dsc2000.jpg'])
        self.assertTrue(config.has_option('photos', 'DSC3000.JPG'))
        self.assertTrue(config.has_option('photos', 'dsc2000.jpg'))


class TestPhoto(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.photo_path = Path(self.temp.name, 'blank.jpg')
        self.output_path = Path(self.temp.name, 'output')
        self.output_path.mkdir()
        src_image = Path(__file__).parent / 'blank.jpg'
        copyfile(str(src_image), str(self.photo_path))

    def tearDown(self):
        self.temp.cleanup()

    def test_short_caption(self):
        photo = Photo(self.photo_path, self.output_path, "Caption")
        self.assertEqual(photo.caption, "Caption")
        self.assertEqual(photo.title, "Caption")

    def test_long_title(self):
        photo = Photo(self.photo_path, self.output_path, "Caption| with text")
        self.assertEqual(photo.caption, "Caption")
        self.assertEqual(photo.title, "Caption with text")

    def test_resize(self):
        photo = Photo(self.photo_path, self.output_path, "Test")
        self.assertTrue(photo.needs_resize())
        photo.resize()
        self.assertTrue((self.output_path / 'large' / 'blank.jpg').exists())
        self.assertTrue((self.output_path / 'thumb' / 'blank.jpg').exists())
        self.assertFalse(photo.needs_resize())
        self.assertEqual(photo.large.url, 'large/blank.jpg')
        self.assertEqual(photo.thumb.url, 'thumb/blank.jpg')
        self.assertEqual(photo.large.size, (1, 1))  # Not larger then original
        self.assertEqual(photo.thumb.size, (1, 1))


class TestInit(unittest.TestCase):
    IMAGES = ['blank-1.jpg', 'blank-2.JPG', 'blank-3.jpeg', 'blank-4.JPEG']

    def setUp(self):
        self.temp = TemporaryDirectory()
        self.gallery_path = Path(self.temp.name)
        self.album_path = self.gallery_path / 'testing-album'
        self.album_path.mkdir()
        src_image = Path(__file__).parent / 'blank.jpg'
        for image in self.IMAGES:
            copyfile(str(src_image), str(self.album_path / image))

    def tearDown(self):
        self.temp.cleanup()

    def test_init_gallery(self):
        generate_gallery_ini(self.gallery_path)
        ini_path = self.gallery_path / 'gallery.ini'
        self.assertTrue(ini_path.exists())
        config = ConfigParser()
        config.read(str(ini_path))
        self.assertEqual(config['gallery']['title'], 'Photo Gallery')
        self.assertEqual(config['gallery']['author'], 'Anonymous')

    def test_init_album(self):
        generate_album_ini(self.album_path)
        ini_path = self.album_path / 'album.ini'
        self.assertTrue(ini_path.exists())
        config = ConfigParser(allow_no_value=True)
        config.read(str(ini_path))
        self.assertEqual(config['album']['title'], 'Testing-album')
        self.assertEqual(config['album']['date'],
                         date.today().strftime("%Y-%m-%d"))
        for image in self.IMAGES:
            self.assertIn(image, config['photos'])
