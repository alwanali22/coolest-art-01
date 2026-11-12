"""
This program deterministically copies art.jpg to entry.png in the output directory after validating its integrity.
"""
import os
import sys
import hashlib

def get_sha256(file_path):
    """Calculate the SHA256 hash of a file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        # Read in blocks to handle large files efficiently
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def main():
    # Find art.jpg beside main.py
    script_dir = os.path.dirname(os.path.abspath(__file__))
    source_path = os.path.join(script_dir, "art.jpg")

    # Validate source exists
    if not os.path.exists(source_path):
        print(f"Error: Source file '{source_path}' does not exist.")
        sys.exit(1)
        
    # Guard for empty source file
    if os.path.getsize(source_path) == 0:
        print(f"Error: Source file '{source_path}' is empty.")
        sys.exit(1)

    # Validate source magic bytes
    with open(source_path, "rb") as f:
        header = f.read(2)
        if header != b'\xff\xd8':
            print(f"Error: File '{source_path}' has invalid JPEG magic bytes.")
            sys.exit(1)

    # Determine output directory
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    try:
        os.makedirs(output_dir, exist_ok=True)
    except OSError as e:
        print(f"Error creating output directory '{output_dir}': {e}")
        sys.exit(1)

    output_path = os.path.join(output_dir, "entry.png")

    # Copy art.jpg to output path
    try:
        with open(source_path, "rb") as src, open(output_path, "wb") as dst:
            dst.write(src.read())
    except IOError as e:
        print(f"Error copying file to '{output_path}': {e}")
        sys.exit(1)

    # Verification
    source_size = os.path.getsize(source_path)
    source_hash = get_sha256(source_path)
    
    # We read back the written file and verify its hash to ensure the copy 
    # process was successful and complete, rather than trusting the write operation alone.
    output_size = os.path.getsize(output_path)
    output_hash = get_sha256(output_path)

    if source_size != output_size or source_hash != output_hash:
        print(f"Error: Verification failed for '{output_path}'.")
        sys.exit(1)

    print(f"Output path: {output_path}")
    print(f"Byte count: {output_size}")
    print(f"SHA256: {output_hash}")

if __name__ == "__main__":
    main()
