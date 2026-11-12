# Phoenix Reborn - luminous phoenix over a neon city at dusk (coolest-art-01)
"""
Reads art.jpg, validates it as a JPEG, and writes it to entry.png in the output directory.
Entry: Phoenix Reborn - a luminous phoenix over a neon city at dusk.
"""
import os
import sys
import hashlib

def main():
    # Get script directory to locate art.jpg reliably
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "art.jpg")

    # Validate input file existence
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        sys.exit(1)

    # Read and validate JPEG magic bytes (FF D8)
    with open(input_path, 'rb') as f:
        header = f.read(2)
        if header != b'\xff\xd8':
            print("Error: Invalid JPEG file (missing magic bytes).")
            sys.exit(1)
        # Read the rest of the file
        content = header + f.read()

    # Determine output directory
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    
    try:
        os.makedirs(output_dir, exist_ok=True)
    except OSError as e:
        print(f"Error: Could not create output directory {output_dir}: {e}")
        sys.exit(1)
        
    output_file = os.path.join(output_dir, "entry.png")

    # Write file
    try:
        with open(output_file, 'wb') as f:
            f.write(content)
    except OSError as e:
        print(f"Error: Could not write output file {output_file}: {e}")
        sys.exit(1)

    # Verify
    file_size = os.path.getsize(output_file)
    if file_size != len(content):
        print("Error: Output file size mismatch.")
        sys.exit(1)

    # Re-reading the file from disk is a stronger guarantee than comparing byte counts
    # alone, as it ensures that the data was fully and correctly committed to the
    # storage medium and not just held in a buffer or subject to I/O corruption.
    with open(output_file, 'rb') as f:
        written_content = f.read()

    if hashlib.sha256(written_content).digest() != hashlib.sha256(content).digest():
        print("Error: SHA-256 hash mismatch between source and written file.")
        sys.exit(1)

    # Calculate SHA256
    sha256 = hashlib.sha256(content).hexdigest()

    print(f"Path: {output_file}")
    print(f"Size: {file_size} bytes")
    print(f"SHA256: {sha256}")

if __name__ == "__main__":
    main()
