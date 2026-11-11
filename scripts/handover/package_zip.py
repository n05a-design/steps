"""
STEPS AI Context Handover - Module 4: ZIP Packaging & Integrity Verification.
"""

import os
import sys
import zipfile
import shutil

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HANDOVER_DIR = os.path.join(REPO_ROOT, "AI_CONTEXT_HANDOVER")
ARTIFACT_DIR = r"C:\Users\Timvo\.gemini\antigravity\brain\b744fb20-9665-4dda-ad3a-675b8210adfa"

ZIP_NAME_USER = "Antigravity Steps Bericht.zip"
ZIP_NAME_SPEC = "AI_CONTEXT_HANDOVER.zip"

dest_paths = [
    os.path.join(REPO_ROOT, ZIP_NAME_USER),
    os.path.join(REPO_ROOT, ZIP_NAME_SPEC),
    os.path.join(ARTIFACT_DIR, ZIP_NAME_USER),
    os.path.join(ARTIFACT_DIR, ZIP_NAME_SPEC)
]

primary_zip = dest_paths[0]
print(f"Creating ZIP archive {primary_zip} from {HANDOVER_DIR}...")

files_to_pack = sorted(os.listdir(HANDOVER_DIR))
with zipfile.ZipFile(primary_zip, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
    for filename in files_to_pack:
        file_path = os.path.join(HANDOVER_DIR, filename)
        if os.path.isfile(file_path):
            # Archive under AI_CONTEXT_HANDOVER/
            arcname = os.path.join("AI_CONTEXT_HANDOVER", filename)
            zf.write(file_path, arcname)
            print(f"  Added: {arcname} ({os.path.getsize(file_path)} bytes)")

# Copy to secondary destinations
for target in dest_paths[1:]:
    os.makedirs(os.path.dirname(target), exist_ok=True)
    shutil.copyfile(primary_zip, target)
    print(f"Copied to: {target} ({os.path.getsize(target)} bytes)")

# Verify primary archive
print("\nVerifying ZIP archive integrity:")
with zipfile.ZipFile(primary_zip, 'r') as zf:
    test_result = zf.testzip()
    if test_result is not None:
        print(f"ERROR: Corrupted file in zip: {test_result}")
        sys.exit(1)
    namelist = zf.namelist()
    print(f"Archive valid! Contained {len(namelist)} files:")
    for name in namelist:
        info = zf.getinfo(name)
        print(f" - {name} ({info.file_size} bytes uncompressed, {info.compress_size} bytes compressed)")

print("\nPackaging completed successfully.")
