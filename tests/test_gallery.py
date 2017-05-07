import unittest
from configparser import ConfigParser
from datetime import date
from pathlib import Path

from kaleidoscope.gallery import generate_gallery_ini, generate_album_ini
from shutil import copyfile
from tempfile import TemporaryDirectory


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
