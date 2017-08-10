from pathlib import Path

from kaleidoscope import gallery
from kaleidoscope.config import GalleryConfigParser


def test_init_gallery(testing_gallery):
    """generate_gallery_ini function should generate valid configuration."""
    gallery_ini = testing_gallery.join('gallery.ini')
    gallery_ini.remove()
    gallery.generate_gallery_ini(Path(testing_gallery))
    assert valid_configuration(gallery_ini, {'gallery': ['title', 'author']})


def test_init_album(testing_gallery):
    """generate_album_ini function should generate configuration with all
    photos found in the directory.
    """
    album_path = testing_gallery.join('testing-album')
    album_ini = album_path.join('album.ini')
    album_ini.remove()
    gallery.generate_album_ini(Path(album_path))
    assert valid_configuration(album_ini, {
        'album': ['title', 'date'],
        'photos': ['Photo1.jpg', 'Photo2.jpg', 'Photo3.jpg', 'Photo4.jpg']
    })


def valid_configuration(path, sections):
    """
    Check if configuration file exists and has specified sections and
    options.
    """
    if not path.exists():
        return False
    config = GalleryConfigParser()
    config.read(str(path))
    for section, options in sections.items():
        if not config.has_section(section):
            return False
        for option in options:
            if not config.has_option(section, option):
                return False
    return True
