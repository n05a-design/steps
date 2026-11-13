"""Check archive identities against real, isolated Git blobs and trees."""

from hashlib import sha256
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory
import unittest

from scripts import verify_registered_git_files as verifier


class RegisteredGitFilesTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name)
        subprocess.run(["git", "init", "-q", str(self.repo)], check=True, capture_output=True)
        self.content = b"first\r\nsecond\n"
        oid = subprocess.check_output(["git", "-C", str(self.repo), "hash-object", "-w", "--stdin"],
                                      input=self.content).strip()
        listing = b"".join(b"100644 blob " + oid + b"\t" + name + b"\n" for name in (b"one.css", b"two.css"))
        self.tree = subprocess.check_output(["git", "-C", str(self.repo), "mktree"], input=listing).decode().strip()
        self.row = {"file_id": "F00001", "path": "one.css", "size_bytes": str(len(self.content)),
                    "sha256": sha256(self.content).hexdigest()}

    def test_exact_shared_blob_and_line_endings(self):
        rows = [self.row, {**self.row, "file_id": "F00002", "path": "two.css"}]
        result = verifier.verify(self.repo, self.tree, rows)
        self.assertEqual(result["counts"], {"MATCH": 2})
        self.assertEqual(result["results"][0]["observed_sha256"], self.row["sha256"])

    def test_hash_size_and_missing_path_are_separate_failures(self):
        for changes, status in (({"sha256": "0" * 64}, "MISMATCH"),
                                ({"size_bytes": "1"}, "MISMATCH"),
                                ({"path": "absent.css"}, "MISSING")):
            with self.subTest(changes=changes):
                result = verifier.verify(self.repo, self.tree, [{**self.row, **changes}])
                self.assertEqual(result["results"][0]["status"], status)

    def test_placeholder_and_duplicate_id_are_rejected(self):
        with self.assertRaises(ValueError):
            verifier.verify(self.repo, self.tree, [{**self.row, "sha256": "PHYSICAL_REVIEW"}])
        with self.assertRaises(ValueError):
            verifier.verify(self.repo, self.tree, [self.row, self.row])

    def test_unavailable_tree_cannot_report_a_match(self):
        with self.assertRaises(subprocess.CalledProcessError):
            verifier.verify(self.repo, "0" * 40, [self.row])
