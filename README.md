# MiniVCS

> Because building your own Git teaches you more than using it.

---

## 📄 Description

**MiniVCS** is a lightweight version control system inspired by Git, built from scratch.  
It helps developers understand how version control works internally by recreating the essential building blocks: staging changes, committing snapshots, and maintaining project history.

Unlike a full Git system, **MiniVCS** focuses purely on:
- Tracking file changes
- Creating commit objects
- Managing references
- Storing data using SHA-1 hashes

This project deepens your understanding of repositories, commits, trees, blobs, and refs — the real foundations behind modern version control.

---

## ✨ Key Features

- **Repository Initialization**: Create a `.minivcs/` hidden folder to store objects and metadata.
- **File Staging**: Hash and store file contents ready for committing.
- **Committing Changes**: Create commits with messages and timestamps linking to staged files.
- **View Commit History**: Traverse through the commit log history.

---

## 🛠️ Tech Stack

- **Language**: Python 3.x
- **Libraries Used**:
  - `os` (file and folder operations)
  - `hashlib` (SHA-1 hashing)
  - `time` (timestamps)

---

## 📂 Project Structure

- `objects/` — stores file contents and commits
- `refs/heads/` — stores branch references
- `HEAD` — points to the current branch

---

## 🚀 Usage

```bash
# Initialize a repository
python main.py init

# Add a file
python main.py add filename.txt

# Commit staged changes
python main.py commit "Initial commit"

# View commit history
python main.py log
