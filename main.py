"""
Art Contest Submission: Entry 'The Storm Stag', Subject 'A colossal stag standing on a cliff edge in a thunderstorm at night, its antlers made of branching lightning, glowing amber eyes'.
Copies art.jpg to entry.png after validating JPEG magic bytes.
Ensures deterministic output for competition entry.
"""
import os
import sys
import hashlib

def main():
    # Resolve source path relative to script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    source_path = os.path.join(script_dir, 'art.jpg')

    # Validate source exists
    if not os.path.exists(source_path):
        print(f"Error: {source_path} not found.")
        sys.exit(1)

    # Validate JPEG magic bytes (FF D8)
    with open(source_path, 'rb') as f:
        header = f.read(2)
        if header != b'\xff\xd8':
            print(f"Error: {source_path} is not a valid JPEG.")
            sys.exit(1)
        # Read the entire file
        f.seek(0)
        content = f.read()

    # Determine output directory
    output_dir = os.environ.get('MAKEFUN_OUTPUT_DIR', '/output')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'entry.png')

    # Write output file
    with open(output_path, 'wb') as f:
        f.write(content)

    # Verify size
    if os.path.getsize(output_path) != len(content):
        print("Error: Size mismatch.")
        sys.exit(1)

    # Comparing the re-read file's hash against the source hash provides a stronger guarantee than just checking the size, as it validates the entire file content, not just its length.
    with open(output_path, 'rb') as f:
        written_content = f.read()
    if hashlib.sha256(written_content).digest() != hashlib.sha256(content).digest():
        print("Error: SHA-256 hash mismatch between source and written file.")
        sys.exit(1)

    # Calculate and display hash
    sha256 = hashlib.sha256(content).hexdigest()
    print(f"Path: {output_path}")
    print(f"Size: {len(content)} bytes")
    print(f"SHA256: {sha256}")

if __name__ == '__main__':
    main()
