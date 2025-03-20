import os
import shutil

def delete_subdirectories(root_dir):
    """
    Recursively deletes all directories and subdirectories within the given directory,
    while keeping the files intact. Also outputs the number of files in the directory.
    """
    file_count = sum(1 for entry in os.scandir(root_dir) if entry.is_file())
    
    for entry in os.scandir(root_dir):
        if entry.is_dir():
            shutil.rmtree(entry.path)
            print(f"Deleted directory: {entry.path}")
    
    print(f"All subdirectories have been deleted. Number of files remaining: {file_count}")

if __name__ == "__main__":
    root_directory = input("Enter the directory path: ").strip()
    if os.path.isdir(root_directory):
        delete_subdirectories(root_directory)
    else:
        print("Invalid directory path.")