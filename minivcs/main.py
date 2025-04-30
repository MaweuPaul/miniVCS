# cli entry point ... handles commands
import sys
import os
from core import init, add, stage

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
    print("  python main.py add example.txt")

def main():
    # Check if .minivcs directory exists for commands other than init
    if len(sys.argv) > 1 and sys.argv[1] != "init" and not os.path.isdir(".minivcs"):
        print("Error: Not a MiniVCS repository (or any of the parent directories)")
        print("Run 'python main.py init' to create a new repository")
        return

    if len(sys.argv) < 2:
        print_usage()
        return

    command = sys.argv[1]

    if command == "init":
        init.create_minivcs_structure()

    elif command == "add":
        if len(sys.argv) < 3:
            print("Error: File path required")
            print("Usage: python main.py add <filename>")
            return
        filename = sys.argv[2]
        add.hash_file_contents(filename)
        
    elif command == "status":
        # Show repository status
        print("On branch master")
        staged_files = stage.list_staged_files()
        
       
        
    elif command == "commit":
        if len(sys.argv) < 3:
            print("Error: Commit message required")
            print("Usage: python main.py commit <message>")
            return
        message = sys.argv[2]
        print(f"Commit functionality not implemented yet.")
        print(f"Would commit with message: {message}")
        
    elif command == "log":
        print("Commit history functionality not implemented yet.")
        
    elif command == "help":
        print_usage()
        
    else:
        print(f"Unknown command: {command}")
        print_usage()

if __name__ == "__main__":
    main()