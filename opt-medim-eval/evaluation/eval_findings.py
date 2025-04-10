import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import argparse

ganmri_inception_corrcoef_data = {
    'Synthetic Percentage': [0, 50, 60, 70, 80, 90, 100],
    'FID': [0.0000654, 97.71195507, 118.8942583, 142.5396132, 163.8193511, 187.5085843, 209.3618621],
    'Precision': [1, 0.62, 0.56, 0.47, 0.4, 0.33, 0.25],
    'Recall': [1, 0.9, 0.89, 0.82, 0.76, 0.69, 0.18],
    'Unbiased FID': [2.013471763, 102.0835921, 113.860521, 131.9922264, 162.933675, 185.2450433, 208.9602984],
    'FC': [1.00000022, 0.747001173, 0.703054373, 0.651567962, 0.608663737, 0.561420789, 0.525153788],
    'Density': [1.004, 0.56, 0.482, 0.368, 0.284, 0.182, 0.092],
    'Coverage': [1, 0.96, 0.93, 0.76, 0.67, 0.49, 0.21]
}

ganmri_dinov2_corrcoef_data = {
    'Synthetic Percentage': [0, 50, 60, 70, 80, 90, 100],
    'FD': [0.000229, 283.5476695, 366.6268334, 445.2439924, 533.3296646, 603.146376, 692.9561115],
    'Precision': [1, 0.71, 0.66, 0.61, 0.55, 0.49, 0.43],
    'Recall': [1, 0.92, 0.92, 0.88, 0.87, 0.8, 0.31],
    'Unbiased FD': [6.644958616, 298.9368115, 339.1634104, 386.7411878, 504.3291383, 546.2169838, 696.5212567],
    'FC': [1.000000071, 0.802613355, 0.768349421, 0.726165703, 0.679205328, 0.628505494, 0.523221794],
    'Density': [1, 0.584, 0.48, 0.418, 0.35, 0.218, 0.158],
    'Coverage': [1, 0.98, 0.9, 0.77, 0.69, 0.38, 0.2]
}

ganmri_swav_corrcoef_data = {
    'Synthetic Percentage': [0, 80, 90, 100],
    'FSD': [-0.00000260227, 1.72551823829725, 1.07266644193531, -0.00000260227],
    'Precision': [1, 0.8125, 0.9125, 1],
    'Recall': [1, 0.975, 0.975, 1],
    'Unbiased FSD': [-0.026181584, 1.699023911, 1.16420987, 0.059362462],
    'Density': [1, 0.785, 0.91, 1],
    'Coverage': [1, 1, 1, 1]
}

dmmri_inception_corrcoef_data = {
    'Synthetic Percentage': [0, 50, 60, 70, 80, 90, 100],
    'FID': [-0.000152408, 83.53286168, 100.3606771, 114.4805349, 138.1902068, 155.750424, 175.3303901],
    'Precision': [0.9, 0.65, 0.6125, 0.575, 0.5125, 0.4125, 0.45],
    'Recall': [0.9, 0.95, 0.875, 0.85, 0.85, 0.6375, 0.375],
    'Unbiased FID': [-5.794803697, 82.01276525, 97.61067271, 113.9103102, 137.3491422, 153.5731494, 170.7922797],
    'FC': [1.000000421, 0.783679559, 0.742143555, 0.703281124, 0.662785039, 0.618545626, 0.552490349],
    'Density': [0.8825, 0.51, 0.415, 0.3875, 0.285, 0.2275, 0.2425],
    'Coverage': [0.9, 0.825, 0.6875, 0.6625, 0.55, 0.4, 0.325]
}

dmmri_dinov2_corrcoef_data = {
    'Synthetic Percentage': [0, 50, 60, 70, 80, 90, 100],
    'FD': [-0.001080752, 720.8734354, 876.7355498, 960.6384922, 1171.32925, 1351.299725, 1595.893447],
    'Precision': [0.9, 0.6875, 0.65, 0.6375, 0.625, 0.5625, 0.55],
    'Recall': [0.9, 0.975, 0.8875, 0.8875, 0.9125, 0.7375, 0.2375],
    'Unbiased FD': [-66.66081855, 701.6441843, 811.5327192, 914.6295131, 1111.290756, 1382.193431, 1561.709643],
    'FC': [1.000000161, 0.838096779, 0.804877489, 0.771862341, 0.733399949, 0.671590925, 0.477439825],
    'Density': [0.88, 0.505, 0.4125, 0.3875, 0.325, 0.2475, 0.2175],
    'Coverage': [0.9, 0.825, 0.675, 0.625, 0.55, 0.3625, 0.15]
}

def calc_correlation_coefficient(corrcoef_data_dict):
    """
    Compute correlation coefficients between the percentage of synthetic training data
    and up to seven user-provided variables:
        - 'Synthetic Percentage'
        - 'FD'
        - 'Precision'
        - 'Recall'
        - 'Unbiased FD'
        - 'FC'
        - 'Density'
        - 'Coverage'

    Parameters:
        data_dict (dict): Dictionary with the following keys:
        - 'Synthetic Percentage'
        - 'FD'
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

    # Compute Pearson correlation with synthetic_percentage
    correlations = {
        var: np.corrcoef(data['Synthetic Percentage'], data[var])[0, 1] for var in variables
    }

    print(pd.Series(correlations, name='correlation_with_synthetic_percentage'))

def main():
    parser = argparse.ArgumentParser(description="Plot findings of evaluation metric experiments")
    parser.add_argument("datasetencoder", type=str, help="Name of the dataset that the experiments were conducted on (e.g. GANMRI, DMMRI)")
    parser.add_argument("--findings", type=str, default="all", help="Type of evaluation metric findings to plot (e.g. corrcoef).")
    args = parser.parse_args()

    if args.datasetencoder == "ganmri-inception":
        if args.findings == "corrcoef":
            calc_correlation_coefficient(ganmri_inception_corrcoef_data)
        if args.findings == "all":
            calc_correlation_coefficient(ganmri_inception_corrcoef_data)
    elif args.datasetencoder == "ganmri-dino":
        if args.findings == "corrcoef":
            calc_correlation_coefficient(ganmri_dinov2_corrcoef_data)
        if args.findings == "all":
            calc_correlation_coefficient(ganmri_dinov2_corrcoef_data)
    elif args.datasetencoder == "ganmri-swav":
        if args.findings == "corrcoef":
            calc_correlation_coefficient(ganmri_swav_corrcoef_data)
        if args.findings == "all":
            calc_correlation_coefficient(ganmri_swav_corrcoef_data)
        calc_correlation_coefficient(ganmri_swav_corrcoef_data)
    elif args.datasetencoder == "dmmri-inception":
        if args.findings == "corrcoef":
            calc_correlation_coefficient(dmmri_inception_corrcoef_data)
        if args.findings == "all":
            calc_correlation_coefficient(dmmri_inception_corrcoef_data)
    elif args.datasetencoder == "dmmri-dino":
        if args.findings == "corrcoef":
            calc_correlation_coefficient(dmmri_dinov2_corrcoef_data)
        if args.findings == "all":
            calc_correlation_coefficient(dmmri_dinov2_corrcoef_data)

if __name__ == '__main__':
    main()