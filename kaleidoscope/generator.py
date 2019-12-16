import os
import shutil
import subprocess
from datetime import date

import imagesize  # type: ignore

from kaleidoscope import model, renderer


SIZES = {'thumb': (330, 220), 'large': (1500, 1000)}


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
        album_output = os.path.join(output, album.name)
        to_resize = [p for p in album.photos if needs_resize(p, album_output)]

        listener.starting_album(album, len(to_resize))
        for photo in to_resize:
            listener.resizing_photo(photo)
            resize(photo, 'thumb', album_output)
            resize(photo, 'large', album_output)
        for photo in album.photos:
            photo.thumb = read_resized_metadata(photo, 'thumb', album_output)
            photo.large = read_resized_metadata(photo, 'large', album_output)
        generate_album_index(gallery, album, album_output)
        listener.finishing_album()


def generate_gallery_index(gallery, output):
    path = os.path.join(output, "index.html")
    context = {'gallery': gallery, 'current_year': date.today().year}
    renderer.render('gallery.html', path, context)


def generate_album_index(gallery, album, album_output):
    context = {
        'album': album,
        'gallery': gallery,
        'current_year': date.today().year,
    }
    index_path = os.path.join(album_output, "index.html")
    renderer.render('album.html', index_path, context)


def resized_image_path(album_output, size_name, photo):
    return os.path.join(album_output, size_name, photo.name)


def needs_resize(photo, album_output):
    thumb_path = resized_image_path(album_output, 'thumb', photo)
    large_path = resized_image_path(album_output, 'large', photo)
    return not os.path.exists(thumb_path) or not os.path.exists(large_path)


def read_resized_metadata(photo, size_name, album_output):
    url = "{}/{}".format(size_name, photo.name)
    size = imagesize.get(resized_image_path(album_output, size_name, photo))
    return model.ResizedImage(url, size)


def resize(photo, size, album_output):
    target = resized_image_path(album_output, size, photo)
    geometry = SIZES[size]
    if not os.path.exists(target):
        os.makedirs(os.path.dirname(target), exist_ok=True)
        subprocess.run(['convert', photo.source_path,
                        '-auto-orient', '-resize', "{}x{}>".format(*geometry),
                        target])


def copy_assets(output):
    assets_path = os.path.join(os.path.dirname(__file__), 'assets')
    assets_output_path = os.path.join(output, 'assets')
    if os.path.exists(assets_output_path):
        shutil.rmtree(assets_output_path)
    shutil.copytree(str(assets_path), str(assets_output_path))
