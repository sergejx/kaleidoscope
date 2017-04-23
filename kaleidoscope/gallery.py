from configparser import ConfigParser
from datetime import datetime
from itertools import groupby
from pathlib import Path
from subprocess import run

import imagesize

from kaleidoscope import generator


class Gallery:
    """Photo gallery -- collection of albums."""
    CONFIG_FILE = 'gallery.ini'

    def __init__(self, path: Path):
        self.path = path

        config = ConfigParser()
        config.read(str(path.joinpath(self.CONFIG_FILE)))

        self.title = config.get('gallery', 'title') or "Photo Gallery"
        self.author = config.get('gallery', 'author')

        self.albums = self._read_albums()
        self.years = self._group_by_years(self.albums)

    def _read_albums(self):
        albums = [Album(self, child) for child in self.path.iterdir()
                  if Album.is_album(child)]
        albums.sort(key=lambda a: a.meta['date'], reverse=True)
        return albums

    def _group_by_years(self, albums):
        years = []
        for year, albums in groupby(albums, lambda a: a.meta['date'].year):
            years.append((year, list(albums)))
        return years

    def generate(self, output_path: Path):
        output_path.mkdir(exist_ok=True)
        generator.copy_assets(output_path)
        generator.render('gallery.html', output_path.joinpath("index.html"),
                         {'gallery': self})
        for album in self.albums:
            album.generate(output_path)


class Album:
    """Photo album."""
    INDEX_FILE = 'album.ini'

    def __init__(self, gallery, path: Path):
        self.gallery = gallery
        self.path = path
        self.name = path.name
        self.meta = {}
        self.photos = []
        index_path = self.path.joinpath(self.INDEX_FILE)
        self._parse_index(index_path)
        if 'date' in self.meta:
            self.meta['date'] = datetime.strptime(self.meta['date'], '%Y-%m-%d')

    @classmethod
    def is_album(cls, path: Path):
        return path.joinpath(cls.INDEX_FILE).exists()

    def _parse_index(self, index_path: Path):
        config = ConfigParser(allow_no_value=True)
        config.read(str(index_path))
        for key, value in config['album'].items():
            self.meta[key] = value
        for filename in config.options('photos'):
            image_path = self.path.joinpath(filename)
            caption = config['photos'][filename] or ""
            photo = Photo(image_path, filename, caption)
            self.photos.append(photo)

    def generate(self, output_base: Path):
        print("Generating album {}".format(self.name))
        album_output = output_base.joinpath(self.name)
        album_output.mkdir(exist_ok=True)
        self._resize_all(album_output)
        generator.render('album.html', album_output.joinpath('index.html'),
                         {'album_info': self.meta,
                          'photos': self.photos,
                          'gallery': self.gallery})

    def _resize_all(self, album_output: Path):
        for photo in self.photos:
            photo.resize(album_output)


class Photo:
    """Photography with metadata and different sizes."""
    def __init__(self, path: Path, name: str, title: str):
        self.path = path
        self.name = name
        self.caption, _, rest = title.partition('|')
        self.title = self.caption + rest

        self.thumb = ResizedImage(self, 'thumb', '300x200')
        self.large = ResizedImage(self, 'large', '1500x1000')

    def resize(self, out_dir: Path):
        self.large.resize(out_dir)
        self.thumb.resize(out_dir)


class ResizedImage:
    """Resized version of the photo."""
    def __init__(self, photo: Photo, size_name: str, geometry: str):
        self.photo = photo
        self.url = '{}/{}'.format(size_name, photo.name)
        self.size_name = size_name
        self.geometry = geometry
        self.size = (0, 0)

    def resize(self, album_output: Path):
        """Actually resize the image."""
        path = album_output.joinpath(self.size_name, self.photo.name)
        if not path.exists():
            print("  resizing " + self.photo.name)
            path.parent.mkdir(exist_ok=True)
            run(['convert', str(self.photo.path),
                 '-resize', self.geometry,
                 '-auto-orient',
                 str(path)])
        self.size = imagesize.get(str(path))


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
