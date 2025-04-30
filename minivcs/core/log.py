import os
import time
import re

def read_commit(commit_hash):
    """Read a commit object and parse its contents."""
    if not commit_hash:
        return None
        
    # Construct the path to the commit object
    obj_path = os.path.join(".minivcs", "objects", commit_hash[:2], commit_hash[2:])
    
    if not os.path.exists(obj_path):
        print(f"Error: commit {commit_hash} not found")
        return None
    
    # Read the commit object
    with open(obj_path, 'rb') as f:
        data = f.read()
    
    # Find the null byte that separates header from content
    null_pos = data.find(b'\x00')
    if null_pos == -1:
        print(f"Error: invalid commit object format for {commit_hash}")
        return None
    
    # Extract the content
    content = data[null_pos + 1:].decode('utf-8')
    
    # Parse the commit content
    commit_info = {}
    message_parts = []
    in_message = False
    
    for line in content.split('\n'):
        if in_message:
            message_parts.append(line)
        elif line.strip() == "":
            in_message = True
        else:
            # Parse headers (tree, parent, author, committer)
            parts = line.split(' ', 1)
            if len(parts) == 2:
                key, value = parts
                commit_info[key] = value
    
    # Combine message lines
    commit_info['message'] = '\n'.join(message_parts)
    
    # Parse timestamp from author or committer
    if 'author' in commit_info:
        match = re.search(r'(\d+) [+-]\d{4}$', commit_info['author'])
        if match:
            commit_info['timestamp'] = int(match.group(1))
    
    return commit_info

def show_log(count=None):
    """Show commit log history."""
    # Get the current branch and its commit
    head_path = os.path.join(".minivcs", "HEAD")
    if not os.path.exists(head_path):
        print("No commits yet")
        return
    
    with open(head_path, 'r') as f:
        head_content = f.read().strip()
    
    # Determine the starting commit hash
    if head_content.startswith("ref: "):
        ref_path = head_content[5:]  # Remove "ref: " prefix
        ref_file = os.path.join(".minivcs", ref_path)
        
        if not os.path.exists(ref_file):
            print("No commits on this branch yet")
            return
            
        with open(ref_file, 'r') as f:
            commit_hash = f.read().strip()
    else:
        # Direct commit hash (detached HEAD)
        commit_hash = head_content
    
    # Walk through commit history
    commits_shown = 0
    while commit_hash and (count is None or commits_shown < count):
        commit_info = read_commit(commit_hash)
        
        if not commit_info:
            break
        
        # Format the timestamp
        timestamp_str = time.strftime(
            "%a %b %d %H:%M:%S %Y", 
            time.localtime(commit_info.get('timestamp', 0))
        )
        
        # Print commit info
        print(f"commit {commit_hash}")
        if 'author' in commit_info:
            author_parts = commit_info['author'].split(' ')
            author = ' '.join(author_parts[:-2])  # Remove timestamp and timezone
            print(f"Author: {author}")
        print(f"Date:   {timestamp_str}")
        print()
        print(f"    {commit_info.get('message', '').strip()}")
        print()
        
        # Move to parent commit
        commit_hash = commit_info.get('parent')
        commits_shown += 1