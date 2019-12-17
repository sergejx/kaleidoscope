from datetime import date

from kaleidoscope import model


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
