# Example modules that we can use to handle files and folders
"""
They Include:
1. pathlib
2. os.Path
3. shutil
4. glob
"""

from pathlib import Path


folder_path = Path("docs") /"notes"
file_path = folder_path / "example.txt"

# Common Operations
if folder_path.exists():
    print(f"Folder exist")
print(f"Error, folder does not exist!")

if file_path.exists():
    print(f"File exist")
print(f"Error, file does not exist!")

# print the file name+extension
print(f'File name and extension in full is: {file_path.name}')

# File name minus the extension
print(f'File name minus extension is: {file_path.stem}')

# print the file extension
print(f'File extension is: {file_path.suffix}')

# Get parent folder of the file
print(f'Parent folder is: {file_path.parent}')

# How to create a file and folder
try:
    folder_path.mkdir(parents=True, exist_ok=True)
except NotADirectoryError as e:
    raise NotADirectoryError(e)

# Write into a file
try:
    file_path.write_text("Hello, world!\nThis is a new file.", encoding="utf-8")
except FileNotFoundError as e:
    raise FileNotFoundError(e)

try:
    with file_path.open(mode="a", encoding="utf-8") as f:
        f.write("\nThis is a new line.")
except FileNotFoundError as e:
    raise FileNotFoundError(e)        

with file_path.open(mode="r", encoding="utf-8") as f:
    content = f.read()
    print(content)
