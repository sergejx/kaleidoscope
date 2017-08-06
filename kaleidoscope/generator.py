import os
import shutil
import subprocess
from datetime import date

import imagesize

from kaleidoscope import model, renderer


SIZES = {'thumb': (300, 200), 'large': (1500, 1000)}


class DefaultListener:
    """Default listener for generator events. Does nothing."""
    def starting_album(self, album, photos_to_process):
        pass

    def finishing_album(self):
        pass

    def resizing_photo(self, photo):
        pass


def generate(gallery, output, listener=DefaultListener()):
    """Generate the whole gallery.

    Events are reported to provided listener (see DefaultListener).
    """
    copy_assets(output)
    generate_gallery_index(gallery, output)
    for album in gallery.albums:
        listener.starting_album(album, len(album.photos))
        for photo in album.photos:
            listener.resizing_photo(photo)
            photo.thumb = make_resized(album.name, photo, 'thumb', output)
            photo.large = make_resized(album.name, photo, 'large', output)
        generate_album_index(gallery, album, output)
        listener.finishing_album()


def generate_gallery_index(gallery, output):
    path = os.path.join(output, "index.html")
    context = {'gallery': gallery, 'current_year': date.today().year}
    renderer.render('gallery.html', path, context)


def generate_album_index(gallery, album, output):
    context = {
        'album': album,
        'gallery': gallery,
        'current_year': date.today().year,
    }
    index_path = os.path.join(output, album.name, "index.html")
    renderer.render('album.html', index_path, context)


def make_resized(album_name, photo, size_name, output):
    target = os.path.join(output, album_name, size_name, photo.name)
    if not os.path.exists(target):
        resize(photo.source_path, target, SIZES[size_name])
    image_url = "{}/{}".format(size_name, photo.name)
    return model.ResizedImage(image_url, imagesize.get(target))


def resize(source, target, geometry):
    os.makedirs(os.path.dirname(target), exist_ok=True)
    subprocess.run(['convert', source, '-auto-orient',
                    '-resize', "{}x{}>".format(*geometry), target])


def copy_assets(output):
    assets_path = os.path.join(os.path.dirname(__file__), 'assets')
    assets_output_path = os.path.join(output, 'assets')
    if os.path.exists(assets_output_path):
        shutil.rmtree(assets_output_path)
    shutil.copytree(str(assets_path), str(assets_output_path))
