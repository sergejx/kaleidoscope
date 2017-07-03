from datetime import date

from kaleidoscope import model


def test_create_gallery():
    """
    When created, gallery should store provided metadata and an empty list of
    albums.
    """
    album = model.Album("1", "1", date.today(), [])
    gallery = model.Gallery("Title", "Author", [album])
    assert gallery.title == "Title"
    assert gallery.author == "Author"
    assert gallery.albums == [album]


def test_group_albums_by_year():
    """Gallery should provide list of albums grouped by year."""
    album_15_1 = model.Album("2015-02", "2015-02", date(2015, 2, 20), [])
    album_15_2 = model.Album("2015-12", "2015-12", date(2015, 12, 5), [])
    album_16_1 = model.Album("2016-02", "2016-02", date(2016, 2, 20), [])
    album_17_1 = model.Album("2017-01", "2017-01", date(2017, 1, 20), [])
    album_17_2 = model.Album("2017-02", "2017-02", date(2017, 2, 20), [])
    album_17_3 = model.Album("2017-05", "2017-30", date(2017, 5, 30), [])
    
    gallery = model.Gallery("", "", [album_15_1, album_16_1, album_17_2,
                                     album_17_1, album_15_2, album_17_3])
    assert gallery.albums_by_year == [
        (2017, [album_17_3, album_17_2, album_17_1]),
        (2016, [album_16_1]),
        (2015, [album_15_2, album_15_1]),
    ]


def test_create_album():
    """
    When created, album should store provided metadata and an empty list of
    photos.
    """
    photo = model.Photo("photo.jpg", "", "", None)
    album = model.Album("folder", "Title", date(2017, 6, 10), [photo])
    assert album.name == "folder"
    assert album.title == "Title"
    assert album.date == date(2017, 6, 10)
    assert album.photos == [photo]


def test_create_photo():
    """
    When created, Photo should store its metadata, source path and empty fields
    for resized versions.
    """
    photo = model.Photo("name.jpg", "caption", "long caption",
                        "gallery/album/name.jpg")
    assert photo.name == "name.jpg"
    assert photo.short_caption == "caption"
    assert photo.long_caption == "long caption"
    assert photo.source_path == "gallery/album/name.jpg"
    assert photo.large is None
    assert photo.thumb is None


def test_create_resized_image():
    """ResizedImage should store URL and image size."""
    image = model.ResizedImage("size/name.jpg", (300, 200))
    assert image.url == "size/name.jpg"
    assert image.size == (300, 200)
