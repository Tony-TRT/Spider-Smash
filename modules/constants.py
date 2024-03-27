from typing import final
from pathlib import Path


BASE_DIR: final(Path) = Path(__file__).resolve().parent.parent
ASSETS_DIR: final(Path) = Path.joinpath(BASE_DIR, "assets")
GRAPHICS_DIR: final(Path) = Path.joinpath(ASSETS_DIR, "graphics")
AUDIO_DIR: final(Path) = Path.joinpath(ASSETS_DIR, "audio")
