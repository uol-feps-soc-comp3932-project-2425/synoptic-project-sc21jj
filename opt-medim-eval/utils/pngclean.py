import os
import re
import argparse

def pngclean(directory, num_to_delete):
    """
    Deletes the first `num_to_delete` slices (sorted by slice number) for each scan 
    in a given directory containing .png files named in the format: [scan]_slice_[number].png
    """

    # Generic pattern to match files like "[any name]_slice_[number].png"
    pattern = re.compile(r'^(.*)_slice_(\d+)\.png$')

    # Dictionary to group slices by base scan name
    scan_slices = {}

    # Iterate through files and group them by base scan name
    for filename in os.listdir(directory):
        match = pattern.match(filename)
        if match:
            scan_name, slice_num = match.groups()
            slice_num = int(slice_num)
            if scan_name not in scan_slices:
                scan_slices[scan_name] = []
            scan_slices[scan_name].append((slice_num, filename))

    # For each scan group, delete the first `num_to_delete` slices
    for scan_name, slices in scan_slices.items():
        # Sort by slice number
        slices.sort()
        # Take first 'num_to_delete' slices
        for slice_num, filename in slices[:num_to_delete]:
            file_path = os.path.join(directory, filename)
            try:
                os.remove(file_path)
                print(f"Deleted: {file_path}")
            except Exception as e:
                print(f"Failed to delete {file_path}: {e}")

def main():
    # Parse path to source directory and number of initial scan slices to delete as command line arguments
    parser = argparse.ArgumentParser(description="Delete the first given number of slices of each scan file in a directory.")
    parser.add_argument("source_dir", type=str, help="Path to the directory containing .png files")
    parser.add_argument("delete_num", type=int, help="Number of initial slices associated with each scan file to be deleted")
    args = parser.parse_args()

    pngclean(args.source_dir, args.delete_num)

if __name__ == "__main__":
    main()
