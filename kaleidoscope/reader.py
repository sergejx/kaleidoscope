from datetime import datetime
import os

from kaleidoscope.config import GalleryConfigParser
from kaleidoscope.model import Gallery, Album, Photo

GALLERY_CONFIG = 'gallery.ini'
ALBUM_CONFIG = 'album.ini'


def read_gallery(path):
    """Read gallery metadata from its source directory."""
    config = GalleryConfigParser()
    config.read(os.path.join(path, GALLERY_CONFIG))
    title = config.get('gallery', 'title') or "Photo Gallery"
    author = config.get('gallery', 'author')
    albums = []
    for child in os.listdir(path):
        child_path = os.path.join(path, child)
        if is_album(child_path):
            albums.append(read_album(child_path))
    return Gallery(title, author, albums)


def read_album(path):
    name = os.path.basename(path)
    config = GalleryConfigParser()
    config.read(os.path.join(path, ALBUM_CONFIG))
    title = config.get('album', 'title')
    date = datetime.strptime(config['album']['date'], '%Y-%m-%d')
    photos = []

    photos_section = config['photos']
    for filename, caption in photos_section.items():
        source_path = os.path.join(path, filename)
        if caption is None:
            caption = ""
        short_caption, _, tail = caption.partition("|")
        long_caption = short_caption + tail
        photo = Photo(filename, short_caption, long_caption, source_path)
        photos.append(photo)

    return Album(name, title, date, photos)


def is_album(path):
    return os.path.exists(os.path.join(path, ALBUM_CONFIG))
