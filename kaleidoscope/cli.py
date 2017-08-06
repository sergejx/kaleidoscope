import argparse
import locale
import os
from pathlib import Path

from tqdm import tqdm

from kaleidoscope.gallery import generate_gallery_ini, generate_album_ini
from kaleidoscope.generator import generate, DefaultListener
from kaleidoscope.reader import read_gallery


def main():
    locale.setlocale(locale.LC_ALL, '')
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--gallery",
        metavar="DIR",
        help="path to the gallery",
        default=".")
    parser.add_argument(
        "--init",
        action='store_true',
        help="generate gallery configuration file")
    parser.add_argument(
        "--init-album",
        metavar="DIR",
        help="generate album configuration file with list of photos")
    args = parser.parse_args()

    if args.init:
        generate_gallery_ini(Path(args.gallery))
    elif args.init_album:
        generate_album_ini(Path(args.gallery).joinpath(args.init_album))
    else:
        gallery = read_gallery(args.gallery)
        output_path = os.path.join(args.gallery, "output")
        generate(gallery, output_path, ProgressReporter())


class ProgressReporter(DefaultListener):
    """Reports progress of gallery generation to a user."""
    def __init__(self):
        self._progressbar = None

    def starting_album(self, album, photos_to_process):
        print("Generating album " + album.title)
        if photos_to_process > 0:
            self._progressbar = tqdm(desc="Resizing", unit="photo",
                                     total=photos_to_process)

    def resizing_photo(self, photo):
        self._progressbar.update(1)

    def finishing_album(self):
        self._progressbar.close()
