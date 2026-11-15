"""Check the logo renderer, the stored brand assets and their app access."""

from hashlib import sha256
import struct
import unittest

from app import brand
from scripts import build_brand_assets as assets


class RendererTests(unittest.TestCase):
    def test_path_commands_follow_svg_rules(self):
        # Implicit line-tos after a move, relative axis commands and closing.
        self.assertEqual(assets.parse_path("M1,2 3,2v2h-2z"),
                         [[(1.0, 2.0), (3.0, 2.0), (3.0, 4.0), (1.0, 4.0)]])
        # Compact Illustrator numbers such as ".5-.5" are separate values.
        self.assertEqual(assets.parse_path("M0,0l.5-.5.5.5Z"),
                         [[(0.0, 0.0), (0.5, -0.5), (1.0, 0.0)]])
        # A smooth curve mirrors the previous control point.
        smooth = assets.parse_path("M0,0c0,10,10,10,10,0s10-10,10,0")[0]
        self.assertEqual(smooth[-1], (20.0, 0.0))
        self.assertLess(min(y for _, y in smooth), -7.0)
        with self.assertRaises(ValueError):
            assets.parse_path("M0,0a5,5,0,0,1,10,0")
        with self.assertRaises(ValueError):
            assets.parse_path("M0,0l5")

    def test_coverage_is_exact_for_partial_pixels_and_shared_edges(self):
        red, blue = (255, 0, 0), (0, 0, 255)
        half = [(red, assets.parse_path("M0,0h1.5v1h-1.5z"))]
        self.assertEqual(assets.render(half, 2, (0.0, 0.0, 2.0)),
                         [bytes((255, 0, 0, 255, 255, 0, 0, 128)), bytes(8)])
        # Two shapes of one colour that meet inside a pixel leave no seam.
        joined = [(blue, assets.parse_path("M0,0h2v2h-2z")),
                  (red, assets.parse_path("M0,0h.5v2h-.5z")),
                  (red, assets.parse_path("M.5,0h1.5v2h-1.5z"))]
        self.assertEqual(assets.render(joined, 2, (0.0, 0.0, 2.0)), [bytes((255, 0, 0, 255)) * 2] * 2)

    def test_png_and_ico_round_trip(self):
        images = {size: [b"".join(bytes((size, row, column, 0 if column == row else 200))
                                  for column in range(size)) for row in range(size)]
                  for size in (16, 64)}
        self.assertEqual(assets.decode_png(assets.encode_png(images[16])), images[16])
        self.assertEqual(assets.decode_ico(assets.encode_ico(images)), images)
        with self.assertRaises(ValueError):
            assets.decode_png(b"not a png")


class StoredAssetTests(unittest.TestCase):
    def test_masters_match_registered_hashes(self):
        for name, digest in assets.MASTER_SHA256.items():
            with self.subTest(master=name):
                self.assertEqual(sha256((assets.MASTERS / name).read_bytes()).hexdigest(), digest)

    def test_stored_assets_match_the_masters(self):
        self.assertEqual(assets.differences(assets.build()), [])

    def test_app_access_resolves_every_stored_size(self):
        self.assertEqual(brand.ASSETS, assets.OUTPUT)
        self.assertEqual((brand.LOGO_SIZES, brand.APP_ICON_SIZES), (assets.LOGO_SIZES, assets.ICON_SIZES))
        for sizes, lookup in ((brand.LOGO_SIZES, brand.logo_path), (brand.APP_ICON_SIZES, brand.app_icon_path)):
            for size in sizes:
                with self.subTest(file=lookup(size).name):
                    header = lookup(size).read_bytes()[16:24]
                    self.assertEqual(struct.unpack(">II", header), (size, size))
        self.assertTrue(set(brand.WINDOW_ICON_SIZES) <= set(brand.APP_ICON_SIZES))
        self.assertTrue(brand.app_icon_ico_path().is_file())

    def test_requested_size_uses_the_next_larger_file(self):
        self.assertEqual(brand.app_icon_path(24).name, "steps-app-icon-32.png")
        self.assertEqual(brand.app_icon_path(4096).name, "steps-app-icon-512.png")
        self.assertEqual(brand.logo_path(1).name, "steps-logo-64.png")
        self.assertEqual(brand.logo_path().name, "steps-logo-128.png")

    def test_window_icon_loads_in_tk(self):
        try:
            import tkinter
        except ImportError as exc:
            self.skipTest(f"No tkinter in this Python: {exc}")
        try:
            root = tkinter.Tk()
        except tkinter.TclError as exc:
            self.skipTest(f"No Tk display available: {exc}")
        try:
            root.withdraw()
            brand.apply_window_icon(root)
            self.assertEqual([photo.width() for photo in root._steps_icon_photos],
                             list(brand.WINDOW_ICON_SIZES))
        finally:
            root.destroy()


if __name__ == "__main__":
    unittest.main()
