"""Check source-chain parsing and live comparisons without network requests."""

import io
from hashlib import sha256
from unittest import TestCase
from unittest.mock import patch

from scripts import verify_css_provenance as provenance


class Response(io.BytesIO):
    url = "https://s4.bcbits.com/player.css"
    headers = {}


class CssProvenanceTests(TestCase):
    def test_saved_embed_requires_matching_stylesheet_and_source_comment(self):
        html = ('<!-- saved from url=(0052)https://bandcamp.com/EmbeddedPlayer/track=1/ -->'
                '<link rel="stylesheet" href="./player.css">')
        self.assertEqual(provenance.saved_embed(html, "player.css"), "https://bandcamp.com/EmbeddedPlayer/track=1/")
        self.assertIsNone(provenance.saved_embed(html, "other.css"))
        self.assertIsNone(provenance.saved_embed(html.replace("bandcamp.com", "example.com"), "player.css"))

    def test_live_origin_hash_and_size_must_both_match(self):
        css = b"synthetic stylesheet\r\n"
        for size, digest, status in ((len(css), sha256(css).hexdigest(), "MATCH"),
                                     (len(css) + 1, sha256(css).hexdigest(), "MISMATCH"),
                                     (len(css), "0" * 64, "MISMATCH")):
            with self.subTest(status=status), patch.object(provenance, "urlopen", side_effect=[
                Response(b'<link rel="stylesheet" href="https://s4.bcbits.com/player.css">'), Response(css),
            ]):
                result = provenance.live_match("https://bandcamp.com/EmbeddedPlayer/track=1/", "player.css", size, digest)
                self.assertEqual(result["status"], status)

    def test_missing_or_foreign_cdn_link_cannot_be_an_origin_match(self):
        for html in (b"<html></html>", b'<link rel="stylesheet" href="https://example.com/player.css">'):
            with self.subTest(html=html), patch.object(provenance, "urlopen", return_value=Response(html)):
                with self.assertRaises(ValueError):
                    provenance.live_match("https://bandcamp.com/EmbeddedPlayer/track=1/", "player.css", 1, "0" * 64)
