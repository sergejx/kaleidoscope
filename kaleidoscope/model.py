from __future__ import annotations

import datetime
from dataclasses import dataclass
from itertools import groupby
from typing import Optional, List, Tuple, Iterable


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


@dataclass
class Album:
    """
    Album information
    - name -- identifier of the album, equal with its folder name
    - title -- displayed title of the album
    - date -- datetime.date for ordering albums in time
    - photos -- ordered list of photos
    """
    name: str
    title: str
    date: datetime.date
    sections: List[Section]

    @property
    def photos(self) -> Iterable[Photo]:
        for section in self.sections:
            for photo in section.photos:
                yield photo


@dataclass
class Section:
    """A named section in the album"""
    name: str
    photos: List[Photo]

    def is_default(self):
        return self.name == 'photos'


@dataclass
class Photo:
    """
    Photo information
    - name -- name of the photo file
    - short_caption
    - long_caption
    - source_path -- path to the source photo
    """
    name: str
    short_caption: str
    long_caption: str
    source_path: str
    large: Optional[ResizedImage] = None
    thumb: Optional[ResizedImage] = None


@dataclass
class ResizedImage:
    """Resized image information: URL and size."""
    url: str
    size: Tuple[int, int]
