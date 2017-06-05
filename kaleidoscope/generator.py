from pathlib import Path

from jinja2 import Environment, PackageLoader
from shutil import copytree, rmtree


def formatdate(value, fmt='%d. %B'):
    return value.strftime(fmt)


class Generator:
    """A collection of functions for generating gallery output."""
    def __init__(self) -> None:
        self.env = Environment(loader=PackageLoader('kaleidoscope', 'templates'))
        self.env.filters['formatdate'] = formatdate

    def render(self, template_name: str, file_path: Path, context: dict) -> None:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        template = self.env.get_template(template_name)
        with file_path.open('w') as output:
            output.write(template.render(context))

    def copy_assets(self, output_path: Path) -> None:
        assets_path = Path(__file__).parent.joinpath('assets')
        assets_output_path = output_path.joinpath('assets')
        if assets_output_path.exists():
            rmtree(str(assets_output_path))
        copytree(str(assets_path), str(assets_output_path))
