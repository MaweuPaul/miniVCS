# MiniVCS

> Because building your own Git teaches you more than using it.

##  Description

**MiniVersionControlSystem** is a lightweight version control system inspired by Git, built from scratch.  
It helps developers understand how version control works internally by recreating the essential building blocks: staging changes, committing snapshots, and maintaining project history.

Unlike a full Git system, **MiniVCS** focuses purely on:

- Tracking file changes
- Creating commit objects
- Managing references
- Storing data using SHA-1 hashes

This project deepens your understanding of repositories, commits, trees, blobs, and refs — the real foundations behind modern version control.

## Key Features

- **Repository Initialization**: Create a `.minivcs/` hidden folder to store objects and metadata.
- **File Staging**: Hash and store file contents ready for committing.
- **Committing Changes**: Create commits with messages and timestamps linking to staged files.
- **View Commit History**: Traverse through the commit log history.

## Tech Stack

- **Language**: Python 3.x
- **Libraries Used**:
  - `os` (file and folder operations)
  - `hashlib` (SHA-1 hashing)
  - `time` (timestamps)
  - `json` (storing staging information)

## Project Structure

.minivcs/ # Repository data
|-- objects/ # Content-addressable storage
|-- refs/
| |-- heads/ # Branch references
|-- HEAD # Current branch pointer
|-- index # Staging area (JSON)

### Code organization

minivcs/
|-- core/ # Core functionality
| |-- init.py # Repository setup
| |-- add.py # File hashing and storage
| |-- stage.py # Staging management
| |-- commit.py # Commit creation
| |-- log.py # History viewing
|-- utils/ # Helper functions
|-- main.py # Command interface

##  Installation

### Install from GitHub

```bash
# Clone the repository
git clone https://github.com/MaweuPaul/miniVCS.git
cd minivcs

# Install the package
pip install -e .

```

##  Usage

After installation, you can use the `minivcs` command from anywhere:

```bash
# Initialize a repository
minivcs init

# Add a file
minivcs add filename.txt

# Check staging status
minivcs status

# Commit staged changes
minivcs commit "Initial commit"

# View commit history
minivcs log
```

##  How It Works

### Content Storage

Files are stored as "blob" objects using SHA-1 hashes of their content, enabling efficient storage where identical content is stored only once.

### Commits and History

Each commit contains:

- A reference to a tree object (snapshot of files)
- A reference to parent commit(s)
- Author information and timestamp
- Commit message

Commits form a chain, with each pointing to its parent, creating a traversable history.

### Staging Area

The staging area (index) tracks which files will be included in the next commit, allowing selective commits of changes.
