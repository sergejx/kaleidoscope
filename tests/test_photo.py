import unittest
from pathlib import Path
from shutil import copyfile
from tempfile import TemporaryDirectory

from kaleidoscope.photo import Photo


class TestPhoto(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.photo_path = Path(self.temp.name, 'blank.jpg')
        self.output_path = Path(self.temp.name, 'output')
        self.output_path.mkdir()
        src_image = Path(__file__).parent / 'data' / 'photo.jpg'
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
        self.assertLessEqual(photo.large.size[0], 1500)
        self.assertLessEqual(photo.large.size[1], 1000)
        self.assertLessEqual(photo.thumb.size[0], 300)
        self.assertLessEqual(photo.thumb.size[1], 200)
