"""
This program copies art.jpg to an output directory and is deterministic.
"""
import os
import sys
import hashlib
from pathlib import Path

def get_sha256(filepath):
    """Calculate the SHA256 hash of a file."""
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

# Resolve path
script_dir = Path(__file__).resolve().parent
art_path = script_dir / 'art.jpg'

# Validate existence and magic bytes
if not art_path.exists():
    print(f"Error: Source file {art_path} not found.", file=sys.stderr)
    sys.exit(1)

if art_path.stat().st_size == 0:
    print(f"Error: Source file {art_path} is empty.", file=sys.stderr)
    sys.exit(1)

with open(art_path, 'rb') as f:
    if f.read(2) != b'\xff\xd8':
        print(f"Error: File {art_path} is not a JPEG.", file=sys.stderr)
        sys.exit(1)

# Output dir
output_dir = Path(os.environ.get('MAKEFUN_OUTPUT_DIR', '/output'))
output_dir.mkdir(parents=True, exist_ok=True)
output_path = output_dir / 'entry.png'

# Copy
with open(art_path, 'rb') as src, open(output_path, 'wb') as dst:
    dst.write(src.read())

# Verify that the destination file's integrity matches the source file's integrity using SHA256 hashing to ensure a successful, bit-perfect copy.
if art_path.stat().st_size != output_path.stat().st_size:
    print(f"Error: Size mismatch between {art_path} and {output_path}.", file=sys.stderr)
    sys.exit(1)

if get_sha256(art_path) != get_sha256(output_path):
    print(f"Error: SHA256 mismatch between {art_path} and {output_path}.", file=sys.stderr)
    sys.exit(1)

print(f"Output: {output_path}")
print(f"Size: {output_path.stat().st_size}")
print(f"SHA256: {get_sha256(output_path)}")
