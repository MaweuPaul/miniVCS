import os
import time
import json
import hashlib
from core import stage

def create_tree_object():
    """
    Create a tree object from the staged files.
    
    Returns:
        str: The SHA-1 hash of the tree object
    """
    # Get all staged files and their hashes
    staged_files = stage.get_staged_files_content()
    
    if not staged_files:
        print("Nothing to commit, working tree clean")
        return None
    
    # Create tree content (format: "blob {hash} {filename}")
    tree_entries = []
    for file_path, file_hash in staged_files.items():
        # Use relative path for the tree
        rel_path = os.path.basename(file_path)
        tree_entries.append(f"blob {file_hash} {rel_path}")
    
    # Sort entries for consistent hashing
    tree_entries.sort()
    
    # Join entries with newlines
    tree_content = "\n".join(tree_entries).encode()
    
    # Add tree header
    header = f"tree {len(tree_content)}".encode() + b'\x00'
    store_content = header + tree_content
    
    # Calculate hash
    sha1_hash = hashlib.sha1(store_content).hexdigest()
    
    # Store the tree object
    dir_path = os.path.join(".minivcs", "objects", sha1_hash[:2])
    os.makedirs(dir_path, exist_ok=True)
    
    obj_path = os.path.join(dir_path, sha1_hash[2:])
    
    if not os.path.exists(obj_path):
        with open(obj_path, 'wb') as f:
            f.write(store_content)
    
    return sha1_hash

def get_current_branch():
    """Get the name of the current branch."""
    head_path = os.path.join(".minivcs", "HEAD")
    
    if not os.path.exists(head_path):
        return "master"  # Default branch
    
    with open(head_path, 'r') as f:
        head_content = f.read().strip()
    
    # HEAD can be a symbolic ref or a commit hash
    if head_content.startswith("ref: "):
        ref_path = head_content[5:]  # Remove "ref: " prefix
        branch_name = ref_path.split('/')[-1]  # Get the branch name
        return branch_name
    
    # If HEAD is a direct commit hash (detached HEAD)
    return "HEAD"

def get_parent_commit():
    """Get the hash of the parent commit (current HEAD)."""
    branch = get_current_branch()
    
    if branch == "HEAD":
        # Handle detached HEAD (read from HEAD file directly)
        head_path = os.path.join(".minivcs", "HEAD")
        with open(head_path, 'r') as f:
            return f.read().strip()
    
    # Read from the branch ref file
    ref_path = os.path.join(".minivcs", "refs", "heads", branch)
    
    if not os.path.exists(ref_path):
        return None  # No previous commit
    
    with open(ref_path, 'r') as f:
        parent_hash = f.read().strip()
    
    return parent_hash

def update_ref(branch_name, commit_hash):
    """Update a branch reference to point to a commit."""
    ref_path = os.path.join(".minivcs", "refs", "heads", branch_name)
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(ref_path), exist_ok=True)
    
    with open(ref_path, 'w') as f:
        f.write(commit_hash)

def create_commit(message, author="MiniVCS User <user@example.com>"):
    """
    Create a commit from staged changes.
    
    Args:
        message (str): The commit message
        author (str): Author information
        
    Returns:
        str: The commit hash or None if commit failed
    """
    # Create tree object from staged files
    tree_hash = create_tree_object()
    
    if not tree_hash:
        return None
    
    # Get parent commit hash
    parent_hash = get_parent_commit()
    
    # Prepare commit content
    timestamp = int(time.time())
    
    commit_lines = [
        f"tree {tree_hash}",
        f"author {author} {timestamp} +0000",
        f"committer {author} {timestamp} +0000"
    ]
    
    # Add parent reference if not the initial commit
    if parent_hash:
        commit_lines.insert(1, f"parent {parent_hash}")
    
    # Add empty line and then commit message
    commit_lines.append("")
    commit_lines.append(message)
    
    # Join with newlines
    commit_content = "\n".join(commit_lines).encode()
    
    # Add commit header
    header = f"commit {len(commit_content)}".encode() + b'\x00'
    store_content = header + commit_content
    
    # Calculate hash
    commit_hash = hashlib.sha1(store_content).hexdigest()
    
    # Store the commit object
    dir_path = os.path.join(".minivcs", "objects", commit_hash[:2])
    os.makedirs(dir_path, exist_ok=True)
    
    obj_path = os.path.join(dir_path, commit_hash[2:])
    
    with open(obj_path, 'wb') as f:
        f.write(store_content)
    
    # Update branch reference
    branch = get_current_branch()
    if branch != "HEAD":
        update_ref(branch, commit_hash)
    else:
        # Update HEAD directly for detached HEAD state
        with open(os.path.join(".minivcs", "HEAD"), 'w') as f:
            f.write(commit_hash)
    
    # Clear staging area
    stage.clear_staging_area()
    
    return commit_hash