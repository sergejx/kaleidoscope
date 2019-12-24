Kaleidoscope
============

A static photo gallery generator.


## Usage ##

1. Create an empty directory for your gallery and generate configuration file:

        kaleidoscope init-gallery

2. Create a sub-directory for the first album and copy your photos into it.
Generate album configuration file:

        kaleidoscope init-album DIR

3. Build the gallery with 

        kaleidoscope build


## Directory structure and file formats ##

Gallery properties are placed in `gallery.ini` file with single section
named `[gallery]` and following keys:

- `title` — title of the gallery
- `author` — author name used in the copyright notice
 
Each album is placed in separate sub-directory with photo files and
configuration file `album.ini`. The file has two sections:

- `[album]` with keys `title` and `date`
- `[photos]` with keys corresponding to file name of photos

You can add title for each photo by specifying value for the key. Pipe `|`
marks the end of short caption (displayed in the index page).

Additionally, you can change order of photos by reordering the keys. 

Kaleidoscope uses standard Python configparse INI format
https://docs.python.org/3/library/configparser.html#supported-ini-file-structure


## Development ##

    git clone https://github.com/sergejx/kaleidoscope.git
    cd kaleidoscope
    python3 -m venv venv        # Creata virtualenv (or use virtualenvwrapper)
    . venv/bin/activate
    pip install --editable .    # Install Kaleidoscope in development mode
    npm install                 # Install JS dependencies
    npm run brunch build        # Build JS and CSS into kaleidoscope/assets

## History ##

Kaleidoscope and its default theme was inspired by ORIGINAL photo gallery
https://github.com/jimmac/original
