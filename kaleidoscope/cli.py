from pathlib import Path

import click
import locale

from kaleidoscope.gallery import Gallery, generate_gallery_ini, generate_album_ini

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
    gallery = Gallery(Path(gallery_path), Path(gallery_path, "output"))
    gallery.generate()


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
