import os
import sys
import numpy as np
import pydicom
from PIL import Image

def dcm2png(dcm_path, png_dir):
    """Convert a .dcm file to a PNG image and save it."""
    os.makedirs(png_dir, exist_ok=True)  # Ensure target directory exists

    try:
        # Load DICOM file
        dicom_data = pydicom.dcmread(dcm_path)
        pixel_array = dicom_data.pixel_array  # Extract image data

        # Normalize data to 8-bit grayscale
        data_min, data_max = np.min(pixel_array), np.max(pixel_array)
        if data_max > data_min:
            pixel_array = (pixel_array - data_min) / (data_max - data_min) * 255.0
        pixel_array = pixel_array.astype(np.uint8)

        # Convert to PIL Image and save
        img_pil = Image.fromarray(pixel_array)
        base_name = os.path.splitext(os.path.basename(dcm_path))[0]
        img_pil.save(os.path.join(png_dir, f"{base_name}.png"))

        print(f"Converted {dcm_path} -> {png_dir}/{base_name}.png")

    except Exception as e:
        print(f"Error converting {dcm_path}: {e}")

def process_real_directory(root_dir):
    """Convert all .dcm files in the 'Real' directory to PNG format."""
    real_dir = os.path.join(root_dir, "Real")
    real_png_dir = os.path.join(root_dir, "realpng")

    if os.path.exists(real_dir):
        for file in os.listdir(real_dir):
            if file.endswith(".dcm"):
                dcm_path = os.path.join(real_dir, file)
                dcm2png(dcm_path, real_png_dir)

def process_synthetic_directory(root_dir):
    """Convert all .dcm files in the 'Synthetic' directory to PNG format."""
    synthetic_dir = os.path.join(root_dir, "Synthetic")
    synthetic_png_dir = os.path.join(root_dir, "syntheticpng")

    if os.path.exists(synthetic_dir):
        for file in os.listdir(synthetic_dir):
            if file.endswith(".dcm"):
                dcm_path = os.path.join(synthetic_dir, file)
                dcm2png(dcm_path, synthetic_png_dir)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python dcm2png.py <root_directory>")
        sys.exit(1)

    root_directory = sys.argv[1]

    # Process both 'Real' and 'Synthetic' directories
    process_real_directory(root_directory)
    process_synthetic_directory(root_directory)

    print("DICOM to PNG conversion complete.")
