import numpy as np
from typing import List
from frechet_coefficient import ImageSimilarityMetrics, load_images
import argparse

# Initialise relevant model, dataset names and scores array
models = ["inceptionv3", "dinov2"]
datasets = ['0-100', '10-90', '20-80', '30-70', '40-60', '50-50', '100-0']
scores = []

def frechet_coefficient(dataset_category):
    # Iterate through all real-synthetic datasets
    for dataset_name in datasets:
        # Initialise paths
        comp_path = f"datasets/{dataset_category}/100set/{dataset_name}"
        const_path = f'datasets/{dataset_category}/100set/100-0'

        # Load images from relevant directories
        images_1: List[np.ndarray] = load_images(path=comp_path) # shape: (num_of_images, height, width, channels)
        images_2: List[np.ndarray] = load_images(path=const_path) # shape: (num_of_images, height, width, channels)

        # Initialise dataset-specific scores array
        dataset_score = []

        # Iterate through relevant encoder models
        for model in models:
            # Initialize the ImageSimilarityMetrics class
            ism = ImageSimilarityMetrics(model=model, verbose=0)

            # Calculate Frechet Coefficient
            fc = ism.calculate_frechet_coefficient(images_1, images_2, batch_size=4)
            
            # Add formatted FC score for specific encoder model to 
            dataset_score.append(f"The Frechet Coefficient, trained on the {model} network, between the '{dataset_name}' dataset and the '100-0' dataset is {fc}")

        # Add dataset FC score strings to scores array
        scores.append(dataset_score)

    # Generate formatted FC score final results string using contents of scores array
    for iterator in range(len(datasets)):
        print(f"{datasets[iterator]} dataset scores:")
        print(scores[iterator][0])
        print(scores[iterator][1], '\n')
        iterator += 1

def main():
    parser = argparse.ArgumentParser(description="Calculate Frechet Coefficient between two imaging datasets")
    parser.add_argument("--ds_category", type=str, help="Dataset category of the imaging data being compared (e.g. GAN-MRI, DM-MRI)")
    args = parser.parse_args()

    frechet_coefficient(args.ds_category)

if __name__ == '__main__':
    main()