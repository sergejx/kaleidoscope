from pathlib import Path
from subprocess import run
from typing import Tuple

import imagesize  # type: ignore


class Photo:
    """Photography with metadata and different sizes."""
    def __init__(self, src: Path, out_dir:Path, title: str) -> None:
        self.path = src
        self.caption, _, rest = title.partition('|')
        self.title = self.caption + rest

        self.thumb = ResizedImage(self.path, out_dir, 'thumb', '300x200>')
        self.large = ResizedImage(self.path, out_dir, 'large', '1500x1000>')

    def needs_resize(self) -> bool:
        return not self.large.exists() or not self.thumb.exists()

    def resize(self) -> None:
        self.large.resize()
        self.thumb.resize()


class ResizedImage:
    """Resized version of the photo."""
    def __init__(self, src: Path, out_dir: Path,
                 size_name: str, geometry: str) -> None:
        self.src = src
        self.path = out_dir / size_name / src.name
        self.url = '{}/{}'.format(size_name, src.name)
        self.geometry = geometry
        self.size = self.read_size() if self.exists() else (0, 0)

    def exists(self) -> bool:
        return self.path.exists()

    def read_size(self) -> Tuple[int, int]:
        return imagesize.get(str(self.path))

    def resize(self) -> None:
        """Actually resize the image."""
        if not self.exists():
            self.path.parent.mkdir(parents=True, exist_ok=True)
            run(['convert', str(self.src),
                 '-resize', self.geometry,
                 '-auto-orient',
                 str(self.path)])
            self.size = self.read_size()
