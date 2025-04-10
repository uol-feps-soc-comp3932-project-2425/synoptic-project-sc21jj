import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import argparse

ganmri_inception_corrcoef_data = {
    'Synthetic Percentage': [0, 50, 60, 70, 80, 90, 100],
    'FD': [],
    'Precision': [],
    'Recall': [],
    'Unbiased FD': [],
    'FC': [],
    'Density': [],
    'Coverage': []
}

ganmri_dinov2_corrcoef_data = {
    'Synthetic Percentage': [0, 50, 60, 70, 80, 90, 100],
    'FD': [],
    'Precision': [],
    'Recall': [],
    'Unbiased FD': [],
    'FC': [],
    'Density': [],
    'Coverage': []
}

ganmri_swav_corrcoef_data = {
    'Synthetic Percentage': [0, 50, 60, 70, 80, 90, 100],
    'FD': [],
    'Precision': [],
    'Recall': [],
    'Unbiased FD': [],
    'Density': [],
    'Coverage': []
}

dmmri_inception_corrcoef_data = {
    'Synthetic Percentage': [0, 50, 60, 70, 80, 90, 100],
    'FD': [],
    'Precision': [],
    'Recall': [],
    'Unbiased FD': [],
    'FC': [],
    'Density': [],
    'Coverage': []
}

dmmri_dinov2_corrcoef_data = {
    'Synthetic Percentage': [0, 50, 60, 70, 80, 90, 100],
    'FD': [],
    'Precision': [],
    'Recall': [],
    'Unbiased FD': [],
    'FC': [],
    'Density': [],
    'Coverage': []
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
    parser.add_argument("dataset", type=str, help="Name of the dataset that the experiments were conducted on (e.g. GANMRI, DMMRI)")
    parser.add_argument("--findings", type=str, default="all", help="Type of evaluation metric findings to plot (e.g. corrcoef).")
    args = parser.parse_args()

    if args.findings == "corrcoef":
        calc_correlation_coefficient()
    elif args.findings == "all":
        calc_correlation_coefficient()

if __name__ == '__main__':
    main()