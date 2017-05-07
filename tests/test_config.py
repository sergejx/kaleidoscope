import unittest

from kaleidoscope.config import GalleryConfigParser


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
