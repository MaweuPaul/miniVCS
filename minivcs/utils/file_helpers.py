# helpers for reading / writing files

# hash file
import hashlib
import os

def hash_file(file_path):
    """generate a sha-1 hash of the file
     arg:
     file path (str): path to the file to be hashed
     return:
     str : sha-1 hash of the file
    """
#  check if file exists
    if not os.path.exists(file_path): 
      raise FileNotFoundError(f"File {file_path} does not exist.")

#    create a sha-1 hash object
    sha1 =hashlib.sha1()

    # read the file in chunks to avoid memory issues with large files
    with open(file_path, "rb") as file:
        chunk =file.read(8192)
        while chunk:
            sha1.update(chunk)
            chunk = file.read(8192)

    return sha1.hexdigest() -
    # 

