from setuptools import setup

setup(
    name='kaleidoscope',
    version='0.1',
    packages=['kaleidoscope'],
    include_package_data=True,
    install_requires=[
        'Click',
        'Jinja2',
        'imagesize',
    ],
    entry_points='''
        [console_scripts]
        kaleidoscope=kaleidoscope.cli:cli
    ''',
)