import os
import hashlib
from core import stage

def hash_file_contents(file_path):
    """Generate a SHA-1 hash of the file content and stage the file."""
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        return None
        
    with open(file_path, 'rb') as f:
        content = f.read()

    # Create blob header
    header = f"blob {len(content)}".encode() + b'\x00'
    store = header + content

    sha1_hash = hashlib.sha1(store).hexdigest()

    # create the directory extracting first two characters of the hash as the directory name
    dir_path = os.path.join(".minivcs", "objects", sha1_hash[:2])
    os.makedirs(dir_path, exist_ok=True)

    # create the file path using the remaining characters of the hash
    obj_path = os.path.join(dir_path, sha1_hash[2:])

    if not os.path.exists(obj_path):
        with open(obj_path, "wb") as out:
            out.write(store)

    # Stage the file by adding it to the index
    success = stage.stage_file(file_path, sha1_hash)

    print(f"Added file: {file_path}")
    print(f"Blob stored at: {obj_path}")
    print(f"SHA-1: {sha1_hash}")
    
    if success:
        print(f"File staged for commit")
    else:
        print(f"Warning: Failed to stage file")
    
    return sha1_hash