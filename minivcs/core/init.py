# Initializes the .minivcs repository
import os

def create_minivcs_structure():
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
create_minivcs_structure()