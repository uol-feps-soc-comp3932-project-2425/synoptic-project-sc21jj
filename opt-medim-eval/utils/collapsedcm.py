import os
import shutil

def collapsedcm(root_dir):
    """
    Recursively moves all .dcm files from subdirectories into the root directory.
    If a file with the same name exists, appends a counter to ensure uniqueness.
    """
    for subdir, _, files in os.walk(root_dir):
        if subdir == root_dir:
            continue  # Skip the root directory itself
        
        for file in files:
            if file.endswith(".dcm"):
                src_path = os.path.join(subdir, file)
                dest_path = os.path.join(root_dir, file)
                
                # Ensure unique filename if conflicts arise
                base, ext = os.path.splitext(file)
                counter = 1
                while os.path.exists(dest_path):
                    dest_path = os.path.join(root_dir, f"{base}_{counter}{ext}")
                    counter += 1
                
                shutil.move(src_path, dest_path)
                print(f"Moved: {src_path} -> {dest_path}")
    
    print("All .dcm files have been moved to the root directory.")

if __name__ == "__main__":
    root_directory = input("Enter the root directory path: ").strip()
    if os.path.isdir(root_directory):
        move_nii_files(root_directory)
    else:
        print("Invalid directory path.")