import os

from jinja2 import Environment, PackageLoader


def formatdate(value, fmt='%d. %B'):
    return value.strftime(fmt)


def render(template_name, file_path, context):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    template = _env.get_template(template_name)
    with open(file_path, 'w') as output:
        output.write(template.render(context))


_env = Environment(loader=PackageLoader('kaleidoscope', 'templates'))
_env.filters['formatdate'] = formatdate
