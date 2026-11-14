"""SMF envelope counterchecks require no optional audit reader."""

import struct
import unittest
from scripts.audit_midi_files import envelope


class MidiAuditTests(unittest.TestCase):
    def fixture(self):
        return b'MThd'+struct.pack('>IHHH',6,0,1,480)+b'MTrk'+struct.pack('>I',4)+b'\0\xff\x2f\0'

    def test_minimal_header_and_track(self):
        self.assertEqual(envelope(self.fixture()),{'format':0,'tracks':1,'division':480})

    def test_truncation_and_declared_track_count_fail(self):
        data=self.fixture()
        for changed in [data[:-1],b'nope'+data[4:],data[:10]+b'\0\x02'+data[12:],data[:12]+b'\0\0'+data[14:]]:
            with self.subTest(data=changed[:14]),self.assertRaises(ValueError):envelope(changed)

    def test_invalid_smpte_division_fails(self):
        data=self.fixture()
        with self.assertRaises(ValueError):envelope(data[:12]+b'\xe0\x28'+data[14:])
