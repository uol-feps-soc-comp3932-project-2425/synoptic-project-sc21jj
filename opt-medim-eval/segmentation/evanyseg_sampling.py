import os
import shutil
import argparse
import random
from pathlib import Path

def sample_files(src_images, src_masks, dst_images, dst_masks, num_samples):
    """Sequentially samples num_samples images and corresponding masks from source to destination directories."""

    # Select the first num_samples image files from the source directory
    image_files = os.listdir(src_images)[:num_samples]  # Select the first num_samples files sequentially
    
    # Copy each selected image and its corresponding mask
    for img_file in image_files:
        mask_file = img_file.replace(".png", "_mask.png")  # Adjust mask file name
        
        # Copy image to destination image directory
        shutil.copy(os.path.join(src_images, img_file), os.path.join(dst_images, img_file))

        # Copy corresponding mask to destination mask directory
        shutil.copy(os.path.join(src_masks, mask_file), os.path.join(dst_masks, mask_file))

def evanyseg_sampling(num_to_sample, percent_real, percent_synth, root, train_ratio):
    # Validate percentages
    if round(percent_real + percent_synth, 2) != 1.0:
        raise ValueError("realpct and synthpct must add up to 1.")
    if not (0 < train_ratio < 1):
        raise ValueError("trn must be a float less than 1.")
    
    tst = 1 - train_ratio
    root_path = Path(root)

    # Construct output directory name based on real and synthetic percentages and ensure it exists
    output_dir = root_path / f"{int(percent_real*100)}-{int(args.synthpct*100)}"
    os.makedirs(output_dir, exist_ok=True)

    # Source directories
    real_images_dir = Path("sampled_realpng/images")
    real_masks_dir = Path("sampled_realpng/masks")
    synth_images_dir = Path("sampled_syntheticpng/images")
    synth_masks_dir = Path("sampled_syntheticpng/masks")

    # Output directories for sampled data
    sample_images_dir = Path("sampleimages")
    sample_masks_dir = Path("samplemasks")
    os.makedirs(sample_images_dir, exist_ok=True)
    os.makedirs(sample_masks_dir, exist_ok=True)
    
    # Compute number of samples per category
    num_real = int(num_to_sample * percent_real)
    num_synth = num_to_sample - num_real  # Ensure total adds to N
    
    # Sample images and masks
    sample_files(real_images_dir, real_masks_dir, sample_images_dir, sample_masks_dir, num_real)
    sample_files(synth_images_dir, synth_masks_dir, sample_images_dir, sample_masks_dir, num_synth)
    
    # Create train/test directories
    train_images_dir = output_dir / "train/images"
    train_masks_dir = output_dir / "train/masks"
    test_images_dir = output_dir / "test/images"
    test_masks_dir = output_dir / "test/masks"
    os.makedirs(train_images_dir, exist_ok=True)
    os.makedirs(train_masks_dir, exist_ok=True)
    os.makedirs(test_images_dir, exist_ok=True)
    os.makedirs(test_masks_dir, exist_ok=True)
    
    # Get full file list
    all_images = sorted(os.listdir(sample_images_dir))
    train_count = int(train_ratio * num_to_sample)
    test_count = num_to_sample - train_count
    
    # Randomly assign images to train/test
    train_files = random.sample(all_images, train_count)
    test_files = [f for f in all_images if f not in train_files]
    
    # Move sampled files to train/test directories
    for file in train_files:
        shutil.move(sample_images_dir / file, train_images_dir / file)
        shutil.move(sample_masks_dir / file.replace(".png", "_mask.png"), train_masks_dir / file.replace(".png", "_mask.png"))
    for file in test_files:
        shutil.move(sample_images_dir / file, test_images_dir / file)
        shutil.move(sample_masks_dir / file.replace(".png", "_mask.png"), test_masks_dir / file.replace(".png", "_mask.png"))
    
    # Cleanup empty directories
    shutil.rmtree(sample_images_dir)
    shutil.rmtree(sample_masks_dir)
    
    # Print train/test split counts
    train_image_count = len(os.listdir(train_images_dir))
    train_mask_count = len(os.listdir(train_masks_dir))
    test_image_count = len(os.listdir(test_images_dir))
    test_mask_count = len(os.listdir(test_masks_dir))
    
    print(f"Processed {num_to_sample} images into {output_dir} successfully.")
    print(f"Train set: {train_image_count} images, {train_mask_count} masks")
    print(f"Test set: {test_image_count} images, {test_mask_count} masks")

def main():
    # Parse total number of samples, percentages of real and synthetic images, path to root directory and training data ratio (optional) as command line arguments
    parser = argparse.ArgumentParser(description="Sample and split images and masks for EvanySeg preprocessing")
    parser.add_argument("n", type=int, help="Total number of images to sample.")
    parser.add_argument("realpct", type=float, help="Percentage of real images (0 to 1).")
    parser.add_argument("synthpct", type=float, help="Percentage of synthetic images (0 to 1).")
    parser.add_argument("root", type=str, help="Root directory where the output should be saved.")
    parser.add_argument("--trn", type=float, default=0.8, help="Training set percentage split (default: 0.8).")
    args = parser.parse_args()

    evanyseg_sampling(args.n, args.realpct, args.synthpct, args.root, args.trn)

if __name__ == "__main__":
    main()

