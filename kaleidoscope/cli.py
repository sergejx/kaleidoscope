import os
from pathlib import Path

import click
import locale
from tqdm import tqdm

from kaleidoscope.reader import read_gallery
from kaleidoscope.gallery import generate_gallery_ini, generate_album_ini
from kaleidoscope.generator import generate, DefaultListener

gallery_path = "."


@click.group()
@click.option('--gallery', type=click.Path())
@click.pass_context
def cli(ctx, gallery):
    locale.setlocale(locale.LC_ALL, '')
    if gallery is not None:
        global gallery_path
        gallery_path = gallery


@cli.command()
def build():
    """Build gallery."""
    gallery = read_gallery(gallery_path)
    output_path = os.path.join(gallery_path, "output")
    generate(gallery, output_path, ProgressReporter())


@cli.command(name='init-gallery')
def init_gallery():
    """Generate gallery configuration file."""
    generate_gallery_ini(Path(gallery_path))


@cli.command(name='init-album')
@click.argument('directory',
                type=click.Path(exists=True, file_okay=False, dir_okay=True))
def init_album(directory):
    """Generate album configuration file with list of photos."""
    generate_album_ini(Path(gallery_path).joinpath(directory))


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
