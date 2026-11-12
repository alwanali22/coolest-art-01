"""
This program deterministically copies the source image to the target output directory as entry.png.
"""
import os
import sys
import hashlib
import shutil

def get_sha256(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def main():
    # Resolve script directory to find art.jpg
    script_dir = os.path.dirname(os.path.abspath(__file__))
    art_path = os.path.join(script_dir, 'art.jpg')
    
    # Check if art.jpg exists
    if not os.path.exists(art_path):
        print(f"Error: Source file {art_path} not found.")
        sys.exit(1)
    
    # Check if art.jpg is empty
    if os.path.getsize(art_path) == 0:
        print(f"Error: Source file {art_path} is empty.")
        sys.exit(1)

    # Validate JPEG magic bytes
    with open(art_path, "rb") as f:
        header = f.read(2)
        if header != b'\xff\xd8':
            print(f"Error: Source file {art_path} is not a valid JPEG.")
            sys.exit(1)

    # Determine output directory
    out_dir = os.environ.get('MAKEFUN_OUTPUT_DIR', './out_default')
    
    try:
        os.makedirs(out_dir, exist_ok=True)
    except OSError as e:
        print(f"Error: Could not create output directory {out_dir}: {e}")
        sys.exit(1)
        
    out_path = os.path.join(out_dir, 'entry.png')
    
    # Copy the file
    try:
        shutil.copyfile(art_path, out_path)
    except IOError as e:
        print(f"Error: Could not copy file to {out_path}: {e}")
        sys.exit(1)
    
    # Verify the output
    # Reading back and hashing the written file to ensure integrity, as copy operations may occasionally fail silently or partially.
    try:
        target_size = os.path.getsize(out_path)
        source_size = os.path.getsize(art_path)
        
        source_sha256 = get_sha256(art_path)
        target_sha256 = get_sha256(out_path)
        
        if source_size != target_size or source_sha256 != target_sha256:
            print(f"Error: Verification failed for {out_path}.")
            sys.exit(1)
    except IOError as e:
        print(f"Error: Could not verify written file {out_path}: {e}")
        sys.exit(1)
        
    print(f"Output path: {out_path}")
    print(f"Byte count: {target_size}")
    print(f"SHA256: {target_sha256}")

if __name__ == "__main__":
    main()
