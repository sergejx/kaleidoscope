from pathlib import Path

from jinja2 import Environment, PackageLoader
from shutil import copytree, rmtree


def formatdate(value, fmt='%d. %B'):
    return value.strftime(fmt)


def render(template_name: str, file_path: Path, context: dict):
    template = _env.get_template(template_name)
    with file_path.open('w') as output:
        output.write(template.render(context))


def copy_assets(output_path: Path):
    assets_path = Path(__file__).parent.joinpath('assets')
    assets_output_path = output_path.joinpath('assets')
    if assets_output_path.exists():
        rmtree(str(assets_output_path))
    copytree(str(assets_path), str(assets_output_path))


_env = Environment(loader=PackageLoader('kaleidoscope', 'templates'))
_env.filters['formatdate'] = formatdate
