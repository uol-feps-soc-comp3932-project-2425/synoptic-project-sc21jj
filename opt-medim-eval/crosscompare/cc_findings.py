import pandas as pd
import numpy as np
import argparse

ganmri_inception_data = {
    "Segmentation Performance Score": [0.0342, 0.0528, 0.0589, 0.0611, 0.0694, 0.0726, 0.0806], 
    "FD": [97.71195507, 163.8193511, 0.0000654, 209.3618621, 187.5085843, 142.5396132, 118.8942583],
    "IS": [2.430245067, 2.430245067, 2.430245067, 2.430245067, 2.430245067, 2.430245067, 2.430245067],
    "Precision": [0.62, 0.4, 1, 0.25, 0.33, 0.47, 0.56],
    "Recall": [0.9, 0.76, 1, 0.18, 0.69, 0.82, 0.89],
    "Unbiased FD": [102.0835921, 162.933675, 2.013471763, 208.9602984, 185.2450433, 131.9922264, 113.860521],
    "FC": [0.747001173, 0.608663737, 1.00000022, 0.525153788, 0.561420789, 0.651567962, 0.703054373],
    "Density": [0.56, 0.284, 1.004, 0.092, 0.182, 0.368, 0.482],
    "Coverage": [0.96, 0.67, 1, 0.21, 0.49, 0.76, 0.93]
}

ganmri_dinov2_data = {
    "Segmentation Performance Score": [0.0342, 0.0528, 0.0589, 0.0611, 0.0694, 0.0726, 0.0806], 
    "FD": [283.5476695, 533.3296646, 0.000229, 692.9561115, 603.146376, 445.2439924, 366.6268334],
    "Precision": [0.71, 0.55, 1, 0.43, 0.49, 0.61, 0.66],
    "Recall": [0.92, 0.87, 1, 0.31, 0.8, 0.88, 0.92],
    "Unbiased FD": [298.9368115, 504.3291383, 6.644958616, 696.5212567, 546.2169838, 386.7411878, 339.1634104],
    "FC": [0.802613355, 0.679205328, 1.000000071, 0.523221794, 0.628505494, 0.726165703, 0.768349421],
    "Density": [0.584, 0.35, 1, 0.158, 0.218, 0.418, 0.48],
    "Coverage": [0.98, 0.69, 1, 0.2, 0.38, 0.77, 0.9]
}

ganmri_swav_data = {
    "Segmentation Performance Score": [0.0528, 0.0589, 0.0611, 0.0694], 
    "FD": [1.725518238, -0.00000260227, -0.00000260227, 1.072666442],
    "Precision": [0.8125, 1, 1, 0.9125],
    "Recall": [0.975, 1, 1, 0.975],
    "Unbiased FD": [1.699023911, -0.026181584, 0.059362462, 1.16420987],
    "Density": [0.785, 1, 1, 0.91],
    "Coverage": [1, 1, 1, 1]
}

dmmri_inception_data = {
    "Segmentation Performance Score": [0.0093, 0.0188, 0.0300, 0.0380, 0.0402, 0.0481, 0.0536], 
    "FD": [114.4805349, 175.3303901, 155.750424, 100.3606771, -0.000152408, 138.1902068, 83.53286168],
    "IS": [1.862494039, 1.862494039, 1.862494039, 1.862494039, 1.862494039, 1.862494039, 1.862494039],
    "Precision": [0.575, 0.45, 0.4125, 0.6125, 0.9, 0.5125, 0.65],
    "Recall": [0.85, 0.375, 0.6375, 0.875, 0.9, 0.85, 0.95],
    "Unbiased FD": [170.7922797, 153.5731494, 137.3491422, 113.9103102, 97.61067271, 82.01276525, -5.794803697],
    "FC": [0.552490349, 0.618545626, 0.662785039, 0.703281124, 0.742143555, 0.783679559, 1.000000421],
    "Density": [0.2425, 0.2275, 0.285, 0.3875, 0.415, 0.51, 0.8825],
    "Coverage": [0.325, 0.4, 0.55, 0.6625, 0.6875, 0.825, 0.9]
}

dmmri_dinov2_data = {
    "Segmentation Performance Score": [0.0093, 0.0188, 0.0300, 0.0380, 0.0402, 0.0481, 0.0536], 
    "FD": [960.6384922, 1595.893447, 1351.299725, 876.7355498, -0.001080752, 1171.32925, 720.8734354],
    "Precision": [0.6375, 0.55, 0.5625, 0.65, 0.9, 0.625, 0.6875],
    "Recall": [0.8875, 0.2375, 0.7375, 0.8875, 0.9, 0.9125, 0.975],
    "Unbiased FD": [1561.709643, 1382.193431, 1111.290756, 914.6295131, 811.5327192, 701.6441843, -66.66081855],
    "FC": [0.477439825, 0.671590925, 0.733399949, 0.771862341, 0.804877489, 0.838096779, 1.000000161],
    "Density": [0.2175, 0.2475, 0.325, 0.3875, 0.4125, 0.505, 0.88],
    "Coverage": [0.15, 0.3625, 0.55, 0.625, 0.675, 0.825, 0.9]
}

def calc_correlation_coefficient(corrcoef_data_dict):
    """
    Compute correlation coefficients between the segmentation performance score
    and up to eight user-provided evaluation metrics associated with a particular real/synthetic subset of a given dataset category for a specific encoder:
        - 'Segmentation Performance Score'
        - 'FD'
        - 'IS'
        - 'Precision'
        - 'Recall'
        - 'Unbiased FD'
        - 'FC'
        - 'Density'
        - 'Coverage'

    Parameters:
        data_dict (dict): Dictionary with the following keys:
        - 'Segmentation Performance Score'
        - 'FD'
        - 'IS'
        - 'Precision'
        - 'Recall'
        - 'Unbiased FD'
        - 'FC'
        - 'Density'
        - 'Coverage'

    Returns:
        pd.Series: Correlation coefficients indexed by variable name.
    """

    # Convert dict to DataFrame
    data = pd.DataFrame(corrcoef_data_dict)

    # Variables to correlate
    variables = list(corrcoef_data_dict.keys())[1:]

    # Compute Pearson correlation with segmentation performance score
    correlations = {
        var: np.corrcoef(data['Segmentation Performance Score'], data[var])[0, 1] for var in variables
    }

    return pd.Series(correlations, name='correlation_with_synthetic_percentage')

def calc_correlation_coefficient_variance(correlation_coefficient_series):
    return

def main():
    parser = argparse.ArgumentParser(description="Generate findings of cross-comparison between evaluation metric values and segmentation performance scores")
    parser.add_argument("dataset", type=str, help="Name of the dataset category the experiments were performed on (e.g. ganmri)")
    parser.add_argument("encoder", type=str, help="Name of the feature extractor encoder used to calculate evaluation metrics")
    parser.add_argument("--findings", type=str, default="all", help="Type of cross-comparison findings to generate (e.g. corrcoef, ccvariance).")
    args = parser.parse_args()

    if args.dataset == "ganmri":
        if args.encoder == "inception":
            corrcoef = calc_correlation_coefficient(ganmri_inception_data)
            if args.findings == "corrcoef":
                print(corrcoef)
            elif args.findings == "ccvariance":
                calc_correlation_coefficient_variance(corrcoef)
            elif args.findings == "all":
                print(corrcoef)
                calc_correlation_coefficient_variance(corrcoef)
        elif args.encoder == "dino":
            corrcoef = calc_correlation_coefficient(ganmri_dinov2_data)
            if args.findings == "corrcoef":
                print(corrcoef)
            elif args.findings == "ccvariance":
                calc_correlation_coefficient_variance(corrcoef)
            elif args.findings == "all":
                print(corrcoef)
                calc_correlation_coefficient_variance(corrcoef)
        elif args.encoder == "swav":
            corrcoef = calc_correlation_coefficient(ganmri_swav_data)
            if args.findings == "corrcoef":
                print(corrcoef)
            elif args.findings == "ccvariance":
                calc_correlation_coefficient_variance(corrcoef)
            elif args.findings == "all":
                print(corrcoef)
                calc_correlation_coefficient_variance(corrcoef)
    elif args.dataset == "dmmri":
        if args.encoder == "inception":
            corrcoef = calc_correlation_coefficient(dmmri_inception_data)
            if args.findings == "corrcoef":
                print(corrcoef)
            elif args.findings == "ccvariance":
                calc_correlation_coefficient_variance(corrcoef)
            elif args.findings == "all":
                print(corrcoef)
                calc_correlation_coefficient_variance(corrcoef)
        elif args.encoder == "dino":
            corrcoef = calc_correlation_coefficient(dmmri_dinov2_data)
            if args.findings == "corrcoef":
                print(corrcoef)
            elif args.findings == "ccvariance":
                calc_correlation_coefficient_variance(corrcoef)
            elif args.findings == "all":
                print(corrcoef)
                calc_correlation_coefficient_variance(corrcoef)

if __name__ == '__main__':
    main()