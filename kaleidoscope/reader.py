import datetime
import os

from kaleidoscope.config import GalleryConfigParser
from kaleidoscope.model import Gallery, Album, Section, Photo

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


def read_album(path: str) -> Album:
    name = os.path.basename(path)
    config = GalleryConfigParser()
    config.read(os.path.join(path, ALBUM_CONFIG))
    title, date = _read_album_info(path, config)

    sections = []
    for section_name in config.sections():
        if section_name != 'album':
            sections.append(_read_sections(section_name, config, path))

    return Album(name, title, date, sections)


def _read_sections(name: str, config: GalleryConfigParser, path: str) -> Section:
    photos = []
    for filename, caption in config[name].items():
        long_caption, short_caption = parse_caption(caption)
        source_path = os.path.join(path, filename)
        photo = Photo(filename, short_caption, long_caption, source_path)
        photos.append(photo)
    return Section(name, photos)


def _read_album_info(path, config):
    try:
        title = config['album']['title']
    except KeyError:
        title = os.path.basename(path)
    try:
        date = parse_date(config['album']['date'])
    except KeyError:
        mtime = os.stat(path).st_mtime
        date = datetime.date.fromtimestamp(mtime)
    return title, date


def parse_caption(caption):
    if caption is None:
        caption = ""
    short_caption, _, tail = caption.partition("|")
    long_caption = short_caption + tail
    return long_caption, short_caption


def parse_date(date_string):
    return datetime.datetime.strptime(date_string, '%Y-%m-%d').date()


def is_album(path):
    return os.path.exists(os.path.join(path, ALBUM_CONFIG))
