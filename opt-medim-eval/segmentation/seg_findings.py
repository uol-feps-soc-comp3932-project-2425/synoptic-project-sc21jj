import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import argparse

# Initialising GANMRI loss data dictionaries

ganmri10_loss_data = {
    "100% real": [3.884354585, 1.358598612, 0.628641151, 0.178619057, 0.28054988, 0.156474985, 0.126280726, 0.04570445, 0.063098292, 0.032721977, 0.025071275, 0.025451113, 0.013941883, 0.014005613, 0.016696906],
    "50% real, 50% synthetic": [5.536033329, 4.005757794, 0.617330238, 0.514298912, 0.545020962, 0.149958007, 0.267717289, 0.262782387, 0.102709049, 0.107502402, 0.065172702, 0.081478671, 0.011430854, 0.025130068, 0.01961707],
    "25% real, 75% synthetic": [4.854657397, 6.889021158, 2.084724441, 1.446450651, 1.312525284, 0.293182973, 0.257969311, 0.116146003, 0.119198211, 0.092602363, 0.022826678, 0.065354352, 0.027486844, 0.067532882, 0.031318476],
    "100% synthetic": [4.111320053, 0.65433497, 0.473223172, 0.829968207, 0.170292642, 0.171400454, 0.207588488, 0.098987298, 0.152942243, 0.031075068, 0.232847019, 0.077056157, 0.067872486, 0.088301135, 0.048726631]
}
ganmri100_loss_data = {
    "100% real": [4.281215727, 0.294141296, 0.233868387, 0.128635405, 0.0711687, 0.098527305, 0.06112668, 0.046478961, 0.044106062, 0.038397775, 0.02781179, 0.027631726, 0.02379076, 0.019170764, 0.017362426],
    "50% real, 50% synthetic": [4.559810326, 0.370020725, 0.198578127, 0.107705253, 0.090481337, 0.081424235, 0.081021538, 0.056198427, 0.046076448, 0.032974259, 0.028514073, 0.024544405, 0.022276453, 0.021035429, 0.020902273],
    "40% real, 60% synthetic": [6.622271568, 0.798955664, 0.228738207, 0.245206127, 0.197986539, 0.123280559, 0.124042915, 0.084727366, 0.067778171, 0.060199031, 0.04429344, 0.037479992, 0.031071002, 0.025301589, 0.02283859],
    "30% real, 70% synthetic": [6.255630866, 0.737353232, 0.42746691, 0.177006533, 0.176088389, 0.178784842, 0.096276989, 0.064748254, 0.064542702, 0.044390005, 0.027056029, 0.031459505, 0.023427459, 0.021379132, 0.014976247],
    "20% real, 80% synthetic": [4.803307459, 0.597851846, 0.387358621, 0.265314814, 0.157584923, 0.176974051, 0.108154455, 0.047715295, 0.042110102, 0.038985068, 0.025870027, 0.017291105, 0.013763809, 0.009369388, 0.008815302],
    "10% real, 90% synthetic": [5.973773718, 0.55383724, 0.320203383, 0.196291646, 0.195392398, 0.135961285, 0.080699529, 0.081212007, 0.059856105, 0.051845521, 0.044061168, 0.040516923, 0.032038143, 0.027502517, 0.024514136],
    "100% synthetic": [6.190061897, 1.110511743, 0.597303919, 0.386488788, 0.263256865, 0.182324842, 0.096339608, 0.121453243, 0.087791484, 0.075079178, 0.061271388, 0.04472199, 0.040552143, 0.032239854, 0.028314398]
}

# Initialising DMMRI loss data dictionaries

dmmri10_loss_data = {
    "100% real": [3.392434488981962, 0.7111654616892338, 0.9370306126656942, 0.526241984218359, 0.24864055146463215, 0.10232592094689608, 0.11927612498402596, 0.07702357694506645, 0.025520379655063152, 0.051077098585665226, 0.040097322256769985, 0.019676443422213197, 0.03128558746539056, 0.017991948407143354, 0.006700481986626983],
    "50% real, 50% synthetic": [3.8366779810748994, 3.442188858985901, 1.5813248977065086, 0.3181213685311377, 0.19480938697233796, 0.055797912646085024, 0.040757432114332914, 0.047082269098609686, 0.020779291226062924, 0.08694605800701538, 0.008276051084976643, 0.03528220753651112, 0.026981898408848792, 0.021172424079850316, 0.011901099409442395],
    "25% real, 75% synthetic": [3.672349989414215, 4.341307699680328, 0.7498690858483315, 0.20546110160648823, 0.10249886801466346, 0.3546401560306549, 0.16270411398727447, 0.11516402231063694, 0.09342485875822604, 0.04299165529664606, 0.029579703230410814, 0.0260923566238489, 0.05226427013985813, 0.01566148425627034, 0.009462561822147109],
    "100% synthetic": [3.825514055788517, 1.5415263921022415, 0.324888595379889, 0.22651267796754837, 0.12235810607671738, 0.09009029506705701, 0.05040239344816655, 0.07346916571259499, 0.05629854369908571, 0.02220966713503003, 0.0314062674442539, 0.021097276359796524, 0.016179344194824807, 0.006810698192566633, 0.005403943709097803]
}

dmmri100_loss_data = {
    "100% real": [5.539423763751984, 0.9537085443735123, 0.2217099666595459, 0.11974759679287672, 0.12875826051458716, 0.10705789644271135, 0.051683900877833366, 0.038420744240283966, 0.04253180045634508, 0.027575295884162188, 0.022365568205714226, 0.02137250709347427, 0.019568929681554437, 0.016656836378388107, 0.017148880753666162],
    "50% real, 50% synthetic": [3.4445362389087677, 0.7395051419734955, 0.5211239047348499, 0.3563954047858715, 0.16740691848099232, 0.1024298882111907, 0.07281391322612762, 0.06059934291988611, 0.03850912256166339, 0.03256700048223138, 0.019754185806959867, 0.017620285041630268, 0.012635818682610989, 0.012256574525963515, 0.009978471440263093],
    "40% real, 60% synthetic": [4.435561314225197, 0.7201649695634842, 0.20569951459765434, 0.20273011550307274, 0.13447883166372776, 0.08092162013053894, 0.040548601653426886, 0.03713997872546315, 0.0320984753780067, 0.03179646655917168, 0.021559279644861817, 0.01823897589929402, 0.014015479711815715, 0.011124552227556705, 0.01276733772829175],
    "30% real, 70% synthetic": [5.690362051129341, 1.195692852139473, 0.5183505564928055, 0.3174996506422758, 0.1895977295935154, 0.18062039464712143, 0.11204780079424381, 0.06631980603560805, 0.059263145085424185, 0.03420107928104699, 0.02369760861620307, 0.025523869087919593, 0.015600061975419521, 0.010651045362465084, 0.009150527359452099],
    "20% real, 80% synthetic": [3.229427456855774, 0.8287445455789566, 0.37679239735007286, 0.26398834865540266, 0.1580454334616661, 0.1362839573994279, 0.09876913670450449, 0.06381992530077696, 0.03579895477741957, 0.03177632577717304, 0.02785901981405914, 0.015811145305633545, 0.011087711667641997, 0.006250167323742062, 0.00706110498867929],
    "10% real, 90% synthetic": [5.934477970004082, 0.9448069185018539, 0.32975141517817974, 0.12373165134340525, 0.15628612414002419, 0.12063391506671906, 0.0596916638314724, 0.06947291176766157, 0.04049823712557554, 0.03584850952029228, 0.03268593875691295, 0.019431950291618705, 0.019518245942890644, 0.017840336775407195, 0.012091631069779396],
    "100% synthetic": [7.1446420550346375, 1.057029975578189, 0.29848636500537395, 0.21606835164129734, 0.1850613234564662, 0.11943125165998936, 0.0479792021214962, 0.05354518489912152, 0.03947695158421993, 0.027035916689783335, 0.020101793576031923, 0.019316612975671887, 0.0137683036737144, 0.012746497755870223, 0.010196073213592172]
}

# Initialising GANMRI performance data dictionaries

ganmri10_perf_data = {
    'Training Data Ratio': ['100% Real', '50/50', '25/75', '100% Synthetic'],
    'True DICE Avg': [0.696, 0.784, 0.844, 0.516],
    'True DICE Var': [0.000450,	0.00986, 0.000166, 0.109],
    'Predicted DICE Avg': [0.682, 0.761, 0.804, 0.429],
    'Predicted DICE Var': [0.0000259, 0.00595, 0.00000162, 0.104],
    'Difference Avg': [0.0142, 0.0236, 0.0402, 0.0871],
    'Difference Var': [0.000142, 0.000491, 0.000253, 0.000046]
}

ganmri100_perf_data = {
    'Training Data Ratio': ['100% Real', '50/50', '40/60', '30/70', '20/80', '10/90', '100% Synthetic'],
    'True DICE Avg': [0.662, 0.590, 0.580, 0.644, 0.605, 0.623, 0.578],
    'True DICE Var': [0.0120, 0.0402, 0.0269, 0.0249, 0.0451, 0.0626, 0.0647],
    'Predicted DICE Avg': [0.602, 0.577, 0.519, 0.594, 0.574, 0.555, 0.546],
    'Predicted DICE Var': [0.0247, 0.0410, 0.0313, 0.0377, 0.0454, 0.0754, 0.0717],
    'Difference Avg': [0.0589, 0.0342, 0.0806, 0.0726, 0.0528, 0.0694, 0.0611],
    'Difference Var': [0.00310, 0.00180, 0.0133, 0.0133, 0.00594, 0.00887, 0.00550]
}

# Initialising DMMRI performance data dictionaries

dmmri10_perf_data = {
    'Training Data Ratio': ['100% Real', '50/50', '25/75', '100% Synthetic'],
    'True DICE Avg': [0.676759177, 0.738314404, 0.718662222, 0.259726892],
    'True DICE Var': [0.002059946, 0.00000122915, 0.007619487, 0.040235188],
    'Predicted DICE Avg': [0.631599665, 0.714648545, 0.701165795, 0.232476816],
    'Predicted DICE Var': [0.00000359083, 0.000000416232, 0.004579389, 0.028548062],
    'Difference Avg': [0.045159512, 0.02366586, 0.017496427, 0.027250076],
    'Difference Var': [0.045160, 0.000000214843, 0.000384885, 0.001000165]
}

dmmri100_perf_data = {
    'Training Data Ratio': ['100% Real', '50/50', '40/60', '30/70', '20/80', '10/90', '100% Synthetic'],
    'True DICE Avg': [0.7913743033434772, 0.6568420542638674, 0.7026464069216937, 0.6093389357654784, 0.6382953766409244, 0.6092338923835579, 0.584668897106879],
    'True DICE Var': [0.006752874156521272, 0.05907587776934072, 0.028744022491537617, 0.04573668215777958, 0.02829917944066556, 0.05292965742538932, 0.06503464553325702],
    'Predicted DICE Avg': [0.7512042611837387, 0.6032403238117695, 0.6646266728639603, 0.6000197663903236, 0.590218323469162, 0.5792833618819714, 0.5658852122724056],
    'Predicted DICE Var': [0.007167805115771584, 0.05651666027262505, 0.025713127821618144, 0.03224539135003943, 0.02717219833754191, 0.052926502050121796, 0.04955060869817619],
    'Difference Avg': [0.040170042159738475, 0.053601730452097894, 0.03801973405773349, 0.009319169375154776, 0.04807705317176243, 0.029950530501586543, 0.018783684834473173],
    'Difference Var': [0.003853763507695141, 0.00700366645422195, 0.004602023765869756, 0.004352758158717241, 0.006579429121842518, 0.0020643015640144096, 0.00502952649356573]
}

# Initialising GANMRI correlation coefficient data dictionaries

ganmri10_corrcoef_data = {
    'Synthetic Percentage': [0, 50, 75, 100],
    'True DICE Avg': [0.696, 0.784, 0.844, 0.516],
    'True DICE Var': [0.000450,	0.00986, 0.000166, 0.109],
    'Predicted DICE Avg': [0.682, 0.761, 0.804, 0.429],
    'Predicted DICE Var': [0.0000259, 0.00595, 0.00000162, 0.104],
    'Difference Avg': [0.0142, 0.0236, 0.0402, 0.0871],
    'Difference Var': [0.000142, 0.000491, 0.000253, 0.000046]
}

ganmri100_corrcoef_data = {
    'Synthetic Percentage': [0, 50, 60, 70, 80, 90, 100],
    'True DICE Avg': [0.662, 0.590, 0.580, 0.644, 0.605, 0.623, 0.578],
    'True DICE Var': [0.0120, 0.0402, 0.0269, 0.0249, 0.0451, 0.0626, 0.0647],
    'Predicted DICE Avg': [0.602, 0.577, 0.519, 0.594, 0.574, 0.555, 0.546],
    'Predicted DICE Var': [0.0247, 0.0410, 0.0313, 0.0377, 0.0454, 0.0754, 0.0717],
    'Difference Avg': [0.0589, 0.0342, 0.0806, 0.0726, 0.0528, 0.0694, 0.0611],
    'Difference Var': [0.00310, 0.00180, 0.0133, 0.0133, 0.00594, 0.00887, 0.00550]
}

# Initialising DMMRI correlation coefficient data dictionaries

dmmri10_corrcoef_data = {
    'Synthetic Percentage': [0, 50, 75, 100],
    'True DICE Avg': [0.676759177, 0.738314404, 0.718662222, 0.259726892],
    'True DICE Var': [0.002059946, 0.00000122915, 0.007619487, 0.040235188],
    'Predicted DICE Avg': [0.631599665, 0.714648545, 0.701165795, 0.232476816],
    'Predicted DICE Var': [0.00000359083, 0.000000416232, 0.004579389, 0.028548062],
    'Difference Avg': [0.045159512, 0.02366586, 0.017496427, 0.027250076],
    'Difference Var': [0.045160, 0.000000214843, 0.000384885, 0.001000165]
}

dmmri100_corrcoef_data = {
    'Synthetic Percentage': [0, 50, 60, 70, 80, 90, 100],
    'True DICE Avg': [0.7913743033434772, 0.6568420542638674, 0.7026464069216937, 0.6093389357654784, 0.6382953766409244, 0.6092338923835579, 0.584668897106879],
    'True DICE Var': [0.006752874156521272, 0.05907587776934072, 0.028744022491537617, 0.04573668215777958, 0.02829917944066556, 0.05292965742538932, 0.06503464553325702],
    'Predicted DICE Avg': [0.7512042611837387, 0.6032403238117695, 0.6646266728639603, 0.6000197663903236, 0.590218323469162, 0.5792833618819714, 0.5658852122724056],
    'Predicted DICE Var': [0.007167805115771584, 0.05651666027262505, 0.025713127821618144, 0.03224539135003943, 0.02717219833754191, 0.052926502050121796, 0.04955060869817619],
    'Difference Avg': [0.040170042159738475, 0.053601730452097894, 0.03801973405773349, 0.009319169375154776, 0.04807705317176243, 0.029950530501586543, 0.018783684834473173],
    'Difference Var': [0.003853763507695141, 0.00700366645422195, 0.004602023765869756, 0.004352758158717241, 0.006579429121842518, 0.0020643015640144096, 0.00502952649356573]
}

def plot_training_loss(loss_data_dict, dataset_name):
    """
    Plots training loss vs. epoch number for different training data ratios.
    
    Parameters:
    - loss_data_dict (dict): Keys are data ratio labels (str), values are lists/arrays of 15 training loss values.
    """
    # Ensure data is in DataFrame format
    epochs = np.arange(1, 16)  # Epochs from 1 to 15
    df = pd.DataFrame(index=epochs)

    for label, losses in loss_data_dict.items():
        if len(losses) != 15:
            raise ValueError(f"Expected 15 loss values for '{label}', but got {len(losses)}.")
        df[label] = losses

    # Plotting values on a line graph
    plt.figure(figsize=(10, 6))
    for column in df.columns:
        plt.plot(df.index, df[column], marker='o', label=column)

    plt.title(f"Training Loss per Epochs for {dataset_name} Datasets")
    plt.xlabel('Epoch')
    plt.ylabel('Training Loss')
    plt.xticks(epochs)
    plt.legend(title='Training Data Ratio')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_segmentation_performance(perf_data_dict, category_col: str = 'Training Data Ratio'):
    """
    Plots three bar charts for True DICE, Predicted DICE, and Difference,
    each showing average and variance with dual y-axes.

    Parameters:
    - perf_data_dict (dict): Dictionary with keys:
        - category_col (e.g. "Training Data Ratio")
        - 'True DICE Avg', 'True DICE Var'
        - 'Predicted DICE Avg', 'Predicted DICE Var'
        - 'Difference Avg', 'Difference Var'
        Each value should be a list of equal length.
    - category_col (str): Name of the category key (x-axis).
    """

    # Ensure all required keys are present
    required_keys = [
        category_col,
        'True DICE Avg', 'True DICE Var',
        'Predicted DICE Avg', 'Predicted DICE Var',
        'Difference Avg', 'Difference Var'
    ]
    missing = [key for key in required_keys if key not in perf_data_dict]
    if missing:
        raise ValueError(f"Missing required keys in data dictionary: {missing}")

    # Ensure all lists are the same length
    lengths = [len(v) for v in perf_data_dict.values()]
    if len(set(lengths)) != 1:
        raise ValueError("All lists in data_dict must be of the same length.")

    # Convert to DataFrame
    df = pd.DataFrame(perf_data_dict)

    # Extract categories and positions
    categories = df[category_col]
    x = np.arange(len(categories))
    width = 0.35

    charts = [
        ('True DICE Avg', 'True DICE Var', 'True DICE Score'),
        ('Predicted DICE Avg', 'Predicted DICE Var', 'Predicted DICE Score'),
        ('Difference Avg', 'Difference Var', 'Difference in DICE Score')
    ]

    # Create a single-row, three-column figure for subplots
    fig, axes = plt.subplots(1, 3, figsize=(18, 6), constrained_layout=True)

    # Generate each subplot
    for i, (avg_key, var_key, title) in enumerate(charts):
        ax = axes[i]
        ax2 = ax.twinx()

        # Plot average values as bars on the left axis
        bars_avg = ax.bar(x - width/2, df[avg_key], width, label='Average', color='tab:blue')

        # Plot variance values as bars on the right axis
        bars_var = ax2.bar(x + width/2, df[var_key], width, label='Variance', color='tab:orange')

        # Set plot titles and labels
        ax.set_title(title)
        ax.set_xlabel(category_col)
        ax.set_xticks(x)
        ax.set_xticklabels(categories, rotation=45, ha='right')
        ax.set_ylabel('Average')
        ax2.set_ylabel('Variance')

        # Combine legends
        lines, labels = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax.legend(lines + lines2, labels + labels2, loc='upper left')

    plt.suptitle('DICE Score Metrics by Training Data Ratio', fontsize=16)
    plt.show()

def calc_correlation_coefficient(corrcoef_data_dict):
    """
    Compute correlation coefficients between the percentage of synthetic training data
    and six user-provided variables:
        - 'Synthetic Percentage'
        - 'True DICE Avg'
        - 'True DICE Var'
        - 'Predicted DICE Avg'
        - 'Predicted DICE Var'
        - 'Difference Avg'
        - 'Difference Var'

    Parameters:
        data_dict (dict): Dictionary with the following keys:
        - 'Synthetic Percentage'
        - 'True DICE Avg'
        - 'True DICE Var'
        - 'Predicted DICE Avg'
        - 'Predicted DICE Var'
        - 'Difference Avg'
        - 'Difference Var'

    Returns:
        pd.Series: Correlation coefficients indexed by variable name.
    """

    # Convert dict to DataFrame
    data = pd.DataFrame(corrcoef_data_dict)

    # List of required columns
    required_cols = [
        'Synthetic Percentage',
        'True DICE Avg',
        'True DICE Var',
        'Predicted DICE Avg',
        'Predicted DICE Var',
        'Difference Avg',
        'Difference Var'
    ]

    # Check for missing keys
    for col in required_cols:
        if col not in data.columns:
            raise ValueError(f"Missing required column: {col}")

    # Variables to correlate
    variables = [
        'True DICE Avg',
        'True DICE Var',
        'Predicted DICE Avg',
        'Predicted DICE Var',
        'Difference Avg',
        'Difference Var'
    ]

    # Compute Pearson correlation with synthetic_percentage
    correlations = {
        var: np.corrcoef(data['Synthetic Percentage'], data[var])[0, 1] for var in variables
    }

    print(pd.Series(correlations, name='correlation_with_synthetic_percentage'))

def main():
    # Parse dataset category/size and type of finding as command line arguments
    parser = argparse.ArgumentParser(description="Generate findings of segmentation tasks")
    parser.add_argument("dataset", type=str, help="Name of the dataset that the experiments were conducted on (e.g. GANMRI10)")
    parser.add_argument("--findings", type=str, default="all", help="Type of segmentation task findings to generate (e.g. loss, performance, corrcoef).")
    args = parser.parse_args()

    if args.findings == "loss":
        plot_training_loss()
    elif args.findings == "performance":
         plot_segmentation_performance()
    elif args.findings == "corrcoef":
        calc_correlation_coefficient_scores()
    elif args.findings == "all":
        plot_training_loss()
        plot_segmentation_performance()
        calc_correlation_coefficient()

if __name__ == '__main__':
    main()