from itertools import groupby


def group_albums_by_year(albums):
    years = []
    for year, albums in groupby(albums, lambda a: a.date.year):
        years.append((year, list(albums)))
    return years


class Gallery:
    """
    Gallery with all metadata including title, author and a list of albums.
    """
    def __init__(self, title, author, albums):
        self.title = title
        self.author = author
        self.albums = sorted(albums, key=lambda a: a.date, reverse=True)
        self.albums_by_year = group_albums_by_year(self.albums)


class Album:
    """
    Album information
    - name -- identifier of the album, equal with its folder name
    - title -- displayed title of the album
    - date -- datetime.date for ordering albums in time
    - photos -- ordered list of photos
    """
    def __init__(self, name, title, date, photos):
        self.name = name
        self.title = title
        self.date = date
        self.photos = photos


class Photo:
    """
    Photo information
    - name -- name of the photo file
    - short_caption
    - long_caption
    - source_path -- path to the source photo
    """
    def __init__(self, name, short_caption, long_caption, source_path):
        self.name = name
        self.short_caption = short_caption
        self.long_caption = long_caption
        self.source_path = source_path
        self.large = None
        self.thumb = None


class ResizedImage:
    """Resized image information: URL and size."""
    def __init__(self, url, size):
        self.url = url
        self.size = size
