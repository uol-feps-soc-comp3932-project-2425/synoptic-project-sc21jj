import os
import random
import shutil
import argparse

def create_dirs(base_dir):
    training_dir = os.path.join(base_dir, 'Training')
    test_dir = os.path.join(base_dir, 'Test')
    
    os.makedirs(training_dir, exist_ok=True)
    os.makedirs(test_dir, exist_ok=True)
    
    return training_dir, test_dir

def split_dataset(base_dir):
    train_ratio = 0.8
    training_dir, test_dir = create_dirs(base_dir)
    
    files = [f for f in os.listdir(base_dir) if os.path.isfile(os.path.join(base_dir, f))]
    
    if not files:
        print(f"No files found in '{base_dir}' to split.")
        return
    
    random.shuffle(files)
    train_size = int(len(files) * train_ratio)
    train_files = files[:train_size]
    test_files = files[train_size:]
    
    for f in train_files:
        shutil.copy(os.path.join(base_dir, f), os.path.join(training_dir, f))
    
    for f in test_files:
        shutil.copy(os.path.join(base_dir, f), os.path.join(test_dir, f))
    
    print(f"Dataset split complete. {len(train_files)} training and {len(test_files)} test files created.")
    
    # Verify all files exist in new locations before deleting original files
    all_files_copied = all(
        os.path.exists(os.path.join(training_dir, f)) or os.path.exists(os.path.join(test_dir, f))
        for f in files
    )
    
    if all_files_copied:
        for f in files:
            os.remove(os.path.join(base_dir, f))
        print("Original files deleted from base directory.")
    else:
        print("Error: Not all files were successfully copied. Cleanup aborted.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split dataset into training and test sets and clean up original files.")
    parser.add_argument("base_directory", type=str, help="Path to the base directory containing the dataset")
    
    args = parser.parse_args()
    
    split_dataset(args.base_directory)