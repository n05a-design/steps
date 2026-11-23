"""Central access to the STEPS logo and app icon for the desktop app.

Every window, dialog and package takes its brand images from here. The files
are rendered from the masters in ``design/brand`` by
``scripts/build_brand_assets.py``.
"""

from __future__ import annotations

from pathlib import Path

__all__ = [
    "APP_ICON_SIZES",
    "LOGO_SIZES",
    "app_icon_ico_path",
    "app_icon_path",
    "apply_window_icon",
    "load_in_app_logo",
    "logo_path",
]

ASSETS = Path(__file__).resolve().parent / "assets/brand"
LOGO_SIZES = (64, 128, 256)
APP_ICON_SIZES = (16, 32, 64, 256, 512)
WINDOW_ICON_SIZES = (256, 64, 32, 16)


def _stored_size(size: int, sizes: tuple[int, ...]) -> int:
    """Choose the smallest stored size that covers ``size``, else the largest."""
    return min((stored for stored in sizes if stored >= size), default=max(sizes))


def logo_path(size: int = 128) -> Path:
    """Return the transparent in-app logo that covers ``size`` pixels."""
    return ASSETS / f"steps-logo-{_stored_size(size, LOGO_SIZES)}.png"


def app_icon_path(size: int = 256) -> Path:
    """Return the app icon with its frame that covers ``size`` pixels."""
    return ASSETS / f"steps-app-icon-{_stored_size(size, APP_ICON_SIZES)}.png"


def app_icon_ico_path() -> Path:
    """Return the Windows icon file for executables and shortcuts."""
    return ASSETS / "steps.ico"


def apply_window_icon(root) -> None:
    """Give a Tk root window and the dialogs it opens later the STEPS app icon."""
    from tkinter import PhotoImage

    photos = [PhotoImage(master=root, file=str(app_icon_path(size))) for size in WINDOW_ICON_SIZES]
    root.iconphoto(True, *photos)
    root._steps_icon_photos = photos  # Tk drops images that Python no longer references.


def load_in_app_logo(master, target_height: int = 28):
    """Load the transparent in-app STEPS logo scaled cleanly for the header."""
    from tkinter import PhotoImage

    photo = PhotoImage(master=master, file=str(logo_path(64)))
    if target_height <= 32 and photo.height() >= 64:
        photo = photo.subsample(2, 2)
    master._steps_logo_photo = photo
    return photo
