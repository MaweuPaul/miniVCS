#!/usr/bin/env python3

import sys
import os
from core import init, add, stage, commit, log

def print_usage():
    """Print usage information for the MiniVCS commands."""
    print("MiniVCS - A lightweight version control system")
    print("\nAvailable commands:")
    print("  init                 - Initialize a new repository")
    print("  add <file>           - Add a file to the staging area")
    print("  status               - Show the status of the working directory and staging area")
    print("  commit <message>     - Commit staged changes with a message")
    print("  log                  - Show commit history")
    print("\nExample:")
    print("  minivcs add example.txt")

def main():
    # Get arguments either from sys.argv or the argument passed to main
    args = sys.argv[1:] if len(sys.argv) > 1 else []
    
    if not args:
        print_usage()
        return
    
    command = args[0]
    
    # Check if .minivcs directory exists for commands other than init
    if command != "init" and not os.path.isdir(".minivcs"):
        print("Error: Not a MiniVCS repository (or any of the parent directories)")
        print("Run 'minivcs init' to create a new repository")
        return

    if command == "init":
        init.create_minivcs_structure()

    elif command == "add":
        if len(args) < 2:
            print("Error: File path required")
            print("Usage: minivcs add <filename>")
            return
        filename = args[1]
        add.hash_file_contents(filename)
        
    elif command == "status":
        # Show repository status
        print("On branch master")
        staged_files = stage.list_staged_files()
        
    elif command == "commit":
        if len(args) < 2:
            print("Error: Commit message required")
            print("Usage: minivcs commit <message>")
            return
        message = args[1]
    
        commit_hash = commit.create_commit(message)
        
        if commit_hash:
            print(f"[{commit.get_current_branch()}] {commit_hash[:7]} {message}")
        
    elif command == "log":
    
        
        count = None
        if len(args) > 1 and args[1].isdigit():
            count = int(args[1])
            
        log.show_log(count)
        
    elif command == "help":
        print_usage()
        
    else:
        print(f"Unknown command: {command}")
        print_usage()

if __name__ == "__main__":
    main()