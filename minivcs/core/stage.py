import os
import time
import json

def stage_file(file_path, hash_value):
    """Stage a file to the staging area"""
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist.")
        return False
        
    # Get the absolute path of the file
    abs_path = os.path.abspath(file_path)


    # Get the file statistics for metadata
    file_stats = os.stat(abs_path)

    # Read the current index file
    index_file = os.path.join(".minivcs", "index")
    
    # Initialize an empty dictionary for staged files
    staged_files = {}
    
    # Read existing index if it exists and has content
    if os.path.exists(index_file) and os.path.getsize(index_file) > 0:
        try:
            with open(index_file, "r") as f:
                content = f.read().strip()
                if content:  # If there's actual content
                    staged_files = json.loads(content)
        except Exception as e:
            print(f"Error reading index file: {e}")
            # Start with an empty dictionary if there's an error
            staged_files = {}
    
    # Add or update the file in the staging area
    staged_files[abs_path] = {
        "hash": hash_value,
        "size": file_stats.st_size,
        "modified_time": file_stats.st_mtime,
        "staged_time": time.time()
    }
    
    # Write the updated index back to disk
    try:
        with open(index_file, "w") as f:
            json.dump(staged_files, f, indent=2)
        print(f"DEBUG: File staged successfully")
        return True
    except Exception as e:
        print(f"Error writing to index file: {e}")
        return False

def list_staged_files():
    """List all files currently staged for commit."""
    index_file = os.path.join(".minivcs", "index")
    
    if not os.path.exists(index_file) or os.path.getsize(index_file) == 0:
        print("No files staged for commit.")
        return []
    
    try:
        with open(index_file, "r") as f:
            content = f.read().strip()
            if not content:
                print("No files staged for commit.")
                return []
            
            staged_files = json.loads(content)
            
        if not staged_files:
            print("No files staged for commit.")
            return []
            
        print("Files staged for commit:")
        for file_path, info in staged_files.items():
            # Convert the path to a relative path if it's in the current directory
            rel_path = os.path.relpath(file_path)
            print(f"  {rel_path} ({info['hash'][:7]})")
            
        return list(staged_files.keys())
    except Exception as e:
        print(f"Error reading index file: {e}")
        return []

def get_staged_files_content():
    """Return a dictionary of staged files with their content hashes."""
    index_file = os.path.join(".minivcs", "index")
    result = {}
    
    if not os.path.exists(index_file) or os.path.getsize(index_file) == 0:
        return result
    
    try:
        with open(index_file, "r") as f:
            content = f.read().strip()
            if not content:
                return result
                
            staged_files = json.loads(content)
            
        for file_path, info in staged_files.items():
            rel_path = os.path.relpath(file_path)
            result[rel_path] = info['hash']
            
        return result
    except Exception as e:
        print(f"Error reading index file: {e}")
        return result

def clear_staging_area():
    """Clear the staging area after a commit."""
    index_file = os.path.join(".minivcs", "index")
    
    # Create an empty index file
    with open(index_file, "w") as f:
        json.dump({}, f)
    
    print("Staging area cleared.")