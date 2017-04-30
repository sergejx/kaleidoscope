from configparser import ConfigParser
from datetime import datetime
from itertools import groupby
from pathlib import Path
from subprocess import run
from typing import Any, Dict, List, Tuple

import click
import imagesize  # type: ignore

from kaleidoscope import generator


class GalleryConfigParser(ConfigParser):
    """ConfigParser with settings for gallery configuration files."""
    def __init__(self) -> None:
        super().__init__(allow_no_value=True)

    def optionxform(self, option: str) -> str:
        # Keep file names keys with '.' case sensitive
        if '.' in option:
            return option
        else:
            return option.lower()

class Gallery:
    """Photo gallery -- collection of albums."""
    CONFIG_FILE = 'gallery.ini'

    def __init__(self, src_path: Path, out_path: Path) -> None:
        self.path = src_path
        self.output = out_path

        config = GalleryConfigParser()
        config.read(str(self.path.joinpath(self.CONFIG_FILE)))

        self.title = config.get('gallery', 'title') or "Photo Gallery"
        self.author = config.get('gallery', 'author')

        self.albums = self._read_albums()
        self.years = self._group_by_years(self.albums)

    def _read_albums(self):
        albums = [Album(self, child) for child in self.path.iterdir()
                  if Album.is_album(child)]
        albums.sort(key=lambda a: a.date, reverse=True)
        return albums

    def _group_by_years(self, albums):
        years = []
        for year, albums in groupby(albums, lambda a: a.date.year):
            years.append((year, list(albums)))
        return years

    def generate(self) -> None:
        self.output.mkdir(exist_ok=True)
        generator.copy_assets(self.output)
        generator.render('gallery.html', self.output.joinpath("index.html"),
                         {'gallery': self})
        for album in self.albums:
            album.generate()


class Album:
    """Photo album."""
    INDEX_FILE = 'album.ini'

    def __init__(self, gallery, path: Path) -> None:
        self.gallery = gallery
        self.path = path
        self.name = path.name
        self.output = gallery.output.joinpath(self.name)
        self.title = None # type: str
        self.date = None  # type: datetime
        self.photos = []  # type: List[Photo]
        index_path = self.path.joinpath(self.INDEX_FILE)
        self._parse_index(index_path)

    @classmethod
    def is_album(cls, path: Path):
        return path.joinpath(cls.INDEX_FILE).exists()

    def _parse_index(self, index_path: Path):
        config = GalleryConfigParser()
        config.read(str(index_path))

        if 'title' in config['album']:
            self.title = config['album']['title']
        else:
            self.title = self.name
        if 'date' in config['album']:
            self.date = datetime.strptime(config['album']['date'], '%Y-%m-%d')
        else:
            self.date = datetime.fromtimestamp(self.path.stat().st_ctime)

        for filename in config.options('photos'):
            caption = config['photos'][filename] or ""
            photo = Photo(self, filename, caption)
            self.photos.append(photo)

    def generate(self) -> None:
        print("Generating album {}".format(self.name))
        self._resize_all()
        self.generate_page()

    def generate_page(self) -> None:
        generator.render('album.html', self.output.joinpath('index.html'),
                         {'album': self, 'gallery': self.gallery})

    def _resize_all(self) -> None:
        photos_for_resize = [p for p in self.photos if p.needs_resize()]
        if photos_for_resize:
            with click.progressbar(photos_for_resize) as bar:
                for photo in bar:  # type: ignore
                    photo.resize()


class Photo:
    """Photography with metadata and different sizes."""
    def __init__(self, album: Album, name: str, title: str) -> None:
        self.album = album
        self.path = album.path.joinpath(name)
        self.name = name
        self.caption, _, rest = title.partition('|')
        self.title = self.caption + rest

        self.thumb = ResizedImage(self, 'thumb', '300x200')
        self.large = ResizedImage(self, 'large', '1500x1000')

    def needs_resize(self) -> bool:
        return not self.large.exists() or not self.thumb.exists()

    def resize(self) -> None:
        self.large.resize()
        self.thumb.resize()


class ResizedImage:
    """Resized version of the photo."""
    def __init__(self, photo: Photo, size_name: str, geometry: str) -> None:
        self.photo = photo
        self.path = photo.album.output.joinpath(size_name, photo.name)
        self.url = '{}/{}'.format(size_name, photo.name)
        self.size_name = size_name
        self.geometry = geometry
        self.size = self.read_size() if self.exists() else (0, 0)

    def exists(self) -> bool:
        return self.path.exists()

    def read_size(self) -> Tuple[int, int]:
        return imagesize.get(str(self.path))

    def resize(self) -> None:
        """Actually resize the image."""
        if not self.exists():
            self.path.parent.mkdir(parents=True, exist_ok=True)
            run(['convert', str(self.photo.path),
                 '-resize', self.geometry,
                 '-auto-orient',
                 str(self.path)])
            self.size = self.read_size()


def generate_gallery_ini(gallery_path: Path):
    with gallery_path.joinpath('gallery.ini').open('w') as output:
        output.write("[gallery]\ntitle: Photo Gallery\nauthor: Anonymous\n")
    print("gallery.ini generated")


def generate_album_ini(album_path: Path):
    album_ini_path = album_path.joinpath('album.ini')

    image_suffixes = ['.jpg', '.jpeg', '.png', '.gif']
    photos = [file.name for file in album_path.iterdir()
              if file.suffix.lower() in image_suffixes]
    photos.sort()

    creation_time = datetime.fromtimestamp(album_path.stat().st_ctime)
    context = {
        'title': album_path.name.capitalize(),
        'date': creation_time.strftime('%Y-%m-%d'),
        'photos': photos,
    }

    generator.render('album.ini', album_ini_path, context)
    print(str(album_ini_path) + " generated")
