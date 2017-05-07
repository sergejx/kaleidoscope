from configparser import ConfigParser


class GalleryConfigParser(ConfigParser):
    """ConfigParser with settings for gallery configuration files."""
    def __init__(self) -> None:
        super().__init__(allow_no_value=True)

    def optionxform(self, option: str) -> str:
        # Keep file names keys with '.' case sensitive
        if '.' in option:
            return option
        else:
            return option.lower()
