# Initializes the .minivcs repository
import os

def create_minivcs_structure():
    # Create basic directory structure first
    os.makedirs(".minivcs/objects", exist_ok=True)
    os.makedirs(".minivcs/refs/heads", exist_ok=True)
    print("Created .minivcs directory structure.")

    # Create HEAD file
    head_path = ".minivcs/HEAD"
    if not os.path.exists(head_path):
        with open(head_path, "w") as head_file:
            head_file.write("ref: refs/heads/master\n")
        print("Created .minivcs/HEAD file.")
    else:
        print(".minivcs/HEAD already exists.")
    
    # Create an empty index file for staging
    index_path = ".minivcs/index"
    if not os.path.exists(index_path):
        with open(index_path, "w") as index_file:
            # Write an empty JSON object
            index_file.write("{}")
        print("Created empty index file for staging.")
    else:
        print(".minivcs/index already exists.")

if __name__ == "__main__":
    create_minivcs_structure()