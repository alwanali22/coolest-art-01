# Entry: The Star Shepherd; Subject: A young cloaked child guiding luminous celestial bodies across a cloud cliff edge under a crescent moon, managed by a staff.
"""
A program to copy art.jpg to entry.png in the output directory.
Validates the JPEG header and ensures deterministic behavior.
"""

import os
import sys
import hashlib

def calculate_sha256(filepath):
    """Calculates the SHA256 hash of a file."""
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while True:
            data = f.read(8192)
            if not data:
                break
            sha256.update(data)
    return sha256.hexdigest()

def main():
    # 1. Resolve source file path
    src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'art.jpg')
    
    # 2. Validate source file
    if not os.path.exists(src_path):
        print(f"Error: {src_path} not found.")
        sys.exit(1)
        
    with open(src_path, 'rb') as f:
        magic = f.read(2)
        if magic != b'\xff\xd8':
            print("Error: Source file does not have valid JPEG magic bytes.")
            sys.exit(1)

    # 3. Determine output directory and path
    output_dir = os.environ.get('MAKEFUN_OUTPUT_DIR', '/output')
    
    # Safety: If we cannot write to /output, try a local 'output'
    try:
        os.makedirs(output_dir, exist_ok=True)
    except OSError:
        # Fallback for testing if /output is not writable
        output_dir = 'output'
        os.makedirs(output_dir, exist_ok=True)
        
    output_path = os.path.join(output_dir, 'entry.png')
    
    # 4. Copy file
    with open(src_path, 'rb') as src, open(output_path, 'wb') as dst:
        dst.write(src.read())
        
    # 5. Verify and print details
    src_hash = calculate_sha256(src_path)
    out_hash = calculate_sha256(output_path)
    
    # Re-reading the written file to calculate a hash provides a stronger
    # guarantee of integrity than merely checking size, as it detects
    # potential data corruption or incomplete writes that could result 
    # in the correct file size but incorrect content.
    if src_hash != out_hash:
        print(f"Error: Integrity check failed! Source hash: {src_hash}, Output hash: {out_hash}")
        sys.exit(1)
        
    out_size = os.path.getsize(output_path)
    
    print(f"Output Path: {output_path}")
    print(f"Byte Count: {out_size}")
    print(f"SHA256: {out_hash}")

if __name__ == '__main__':
    main()
