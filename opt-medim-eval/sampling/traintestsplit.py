import os
import random
import shutil
import argparse

def create_dirs(base_dir, train_ratio):
    split_name = f"{int(train_ratio * 100)}-{int((1 - train_ratio) * 100)}"
    training_test_dir = os.path.join(base_dir, 'Training-test', split_name)
    training_dir = os.path.join(training_test_dir, 'Training')
    test_dir = os.path.join(training_test_dir, 'Test')
    
    os.makedirs(training_dir, exist_ok=True)
    os.makedirs(test_dir, exist_ok=True)
    
    return training_dir, test_dir

def split_dataset(base_dir, sample_size=250, train_ratio=0.8):
    real_dir = os.path.join(base_dir, 'Real', 'sampled_realpng')
    training_dir, test_dir = create_dirs(base_dir, train_ratio)
    
    if not os.path.exists(real_dir):
        print(f"Directory '{real_dir}' does not exist.")
        return
    
    files = [f for f in os.listdir(real_dir) if os.path.isfile(os.path.join(real_dir, f))]
    
    if len(files) < sample_size:
        print(f"Not enough files in target directory. Found {len(files)}, required {sample_size}.")
        return
    
    random.shuffle(files)
    selected_files = files[:sample_size]
    
    train_size = int(sample_size * train_ratio)
    train_files = selected_files[:train_size]
    test_files = selected_files[train_size:]
    
    for f in train_files:
        shutil.copy(os.path.join(real_dir, f), os.path.join(training_dir, f))
    
    for f in test_files:
        shutil.copy(os.path.join(real_dir, f), os.path.join(test_dir, f))
    
    print(f"Dataset split complete. {len(train_files)} training and {len(test_files)} test files created.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split dataset into training and test sets.")
    parser.add_argument("--train_ratio", type=float, default=0.8, help="Training set ratio (default: 0.8)")
    args = parser.parse_args()
    
    base_directory = '.'  # Root directory
    split_dataset(base_directory, train_ratio=args.train_ratio)