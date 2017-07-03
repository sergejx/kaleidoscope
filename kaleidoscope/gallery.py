from datetime import datetime
from pathlib import Path

from kaleidoscope import renderer


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

    renderer.render('album.ini', str(album_ini_path), context)
    print(str(album_ini_path) + " generated")
