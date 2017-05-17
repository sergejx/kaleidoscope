from configparser import ConfigParser
from datetime import date, datetime
from pathlib import Path
from shutil import copyfile
from tempfile import TemporaryDirectory
from unittest import TestCase, mock

from kaleidoscope import gallery


class TestAlbum(TestCase):
    maxDiff = None
    GALLERY_PATH = Path(__file__).parent / 'testing-gallery'
    ALBUM_PATH = GALLERY_PATH / 'testing-album'
    OUTPUT_PATH = GALLERY_PATH / 'output'
    ALBUM_OUTPUT = OUTPUT_PATH / 'testing-album'

    @mock.patch('kaleidoscope.photo.Photo.__init__')
    def test_read_album(self, mock_photo_init):
        mock_photo_init.return_value = None
        gallery_mock = mock.MagicMock()
        gallery_mock.output = self.OUTPUT_PATH

        album = gallery.Album(gallery_mock, self.ALBUM_PATH)

        self.assertTrue(mock_photo_init.called)
        self.assertEqual(album.name, 'testing-album')
        self.assertEqual(album.path, self.ALBUM_PATH)
        self.assertEqual(album.output, self.ALBUM_OUTPUT)
        self.assertEqual(album.title, "Testing Album")
        self.assertEqual(album.date, datetime(2017, 5, 15, 0, 0))
        self.assertEqual(len(album.photos), 4)
        self.assertListEqual(mock_photo_init.call_args_list, [
            mock.call(self.ALBUM_PATH / '1.jpg', self.ALBUM_OUTPUT, ''),
            mock.call(self.ALBUM_PATH / '2.jpg', self.ALBUM_OUTPUT, 'Caption'),
            mock.call(self.ALBUM_PATH / '3.jpg', self.ALBUM_OUTPUT, 'Long caption'),
            mock.call(self.ALBUM_PATH / '4.jpg', self.ALBUM_OUTPUT,
                      'Long caption| with hidden part')
        ])


class TestInit(TestCase):
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
        gallery.generate_gallery_ini(self.gallery_path)
        ini_path = self.gallery_path / 'gallery.ini'
        self.assertTrue(ini_path.exists())
        config = ConfigParser()
        config.read(str(ini_path))
        self.assertEqual(config['gallery']['title'], 'Photo Gallery')
        self.assertEqual(config['gallery']['author'], 'Anonymous')

    def test_init_album(self):
        gallery.generate_album_ini(self.album_path)
        ini_path = self.album_path / 'album.ini'
        self.assertTrue(ini_path.exists())
        config = ConfigParser(allow_no_value=True)
        config.read(str(ini_path))
        self.assertEqual(config['album']['title'], 'Testing-album')
        self.assertEqual(config['album']['date'],
                         date.today().strftime("%Y-%m-%d"))
        for image in self.IMAGES:
            self.assertIn(image, config['photos'])
