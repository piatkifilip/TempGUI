import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
from sklearn.pipeline import Pipeline
from sklearn.metrics import make_scorer  # Import make_scorer
from skopt import BayesSearchCV
from skopt.space import Real
import numpy as np
import datetime
import joblib

# Function to load data from an Excel file
def load_data(file_name):
    return pd.concat(pd.read_excel(file_name, sheet_name=None), ignore_index=True)

# Function to calculate the slope given a series of temperature readings
def calculate_slope(temperature_series):
    return np.gradient(temperature_series)

# Function to calculate the ratio between two temperature readings
def calculate_ratio(temp1, temp2):
    with np.errstate(divide='ignore', invalid='ignore'):
        ratio = np.true_divide(temp1, temp2)
        ratio[ratio == np.inf] = 0
        ratio = np.nan_to_num(ratio)
    return ratio

# Combine data from multiple files
data_10C = load_data('10C.xlsx')
data_3C = load_data('3C.xlsx')
data_5C = load_data('5C.xlsx')
data_1C = load_data('1C.xlsx')
combined_data = pd.concat([data_10C, data_5C,data_3C, data_1C], ignore_index=True)

# Drop rows with NaN values in either features or target
combined_data = combined_data.dropna(subset=['HeadTemp1', 'HeadTemp2', 'TunnelTemp'])

# Calculate slopes for HeadTemp1 and HeadTemp2
combined_data['Slope_HeadTemp1'] = calculate_slope(combined_data['HeadTemp1'])
combined_data['Slope_HeadTemp2'] = calculate_slope(combined_data['HeadTemp2'])

# Calculate ratio of HeadTemp1 to HeadTemp2
combined_data['Ratio_HeadTemp1_HeadTemp2'] = calculate_ratio(combined_data['HeadTemp1'], combined_data['HeadTemp2'])

# Prepare the features and target variable
X = combined_data[['HeadTemp1', 'HeadTemp2', 'Slope_HeadTemp1', 'Slope_HeadTemp2', 'Ratio_HeadTemp1_HeadTemp2']]
y = combined_data['TunnelTemp']

# Calculate the delta between HeadTemp1 and HeadTemp2
combined_data['Delta_Temp1_Temp2'] = combined_data['HeadTemp1'] - combined_data['HeadTemp2']

# Segment the data based on delta
data_case_1 = combined_data[combined_data['Delta_Temp1_Temp2'] > 3]
data_case_2 = combined_data[(combined_data['Delta_Temp1_Temp2'] <= 3) & (combined_data['Delta_Temp1_Temp2'] >= -3)]
data_case_3 = combined_data[combined_data['Delta_Temp1_Temp2'] < -23]

def custom_scorer(y_true, y_pred):
    weights = np.where((y_true >= 55) & (y_true <= 59), 25, 1)  # Apply more weight within the 55-59 range
    return np.average(np.abs(y_true - y_pred), weights=weights)

# Convert custom_scorer into a scorer function for use in BayesSearchCV
weighted_scorer = make_scorer(custom_scorer, greater_is_better=False)

# Define a function to train and print the model equation for a given dataset
def train_and_print_equation(data, case_name):
    X_case = data[['HeadTemp1', 'HeadTemp2', 'Slope_HeadTemp1', 'Slope_HeadTemp2', 'Ratio_HeadTemp1_HeadTemp2']]
    y_case = data['TunnelTemp']

    X_train, X_test, y_train, y_test = train_test_split(X_case, y_case, test_size=0.2, random_state=42)

    model_pipeline = Pipeline([
        ('ridge', Ridge())
    ])

    search_spaces = {
        'ridge__alpha': Real(1e-6, 1e+6, prior='log-uniform')
    }

    bayes_search = BayesSearchCV(
        estimator=model_pipeline,
        search_spaces=search_spaces,
        n_iter=200,
        cv=20,
        n_jobs=-1,
        scoring=weighted_scorer,  # Pass the weighted_scorer object
        random_state=24
    )

    bayes_search.fit(X_train, y_train)

    best_model = bayes_search.best_estimator_
    best_params = bayes_search.best_params_
    best_score = bayes_search.best_score_
    score = best_model.score(X_test, y_test)

    print(f'Best Model for {case_name} Test R^2 Score: {score}')
    print(f'Best Model Parameters for {case_name}: {best_params}')

    ridge_model = best_model.named_steps['ridge']
    coefficients = ridge_model.coef_
    intercept = ridge_model.intercept_
    feature_names = X_case.columns
    write_coefficients_to_file(case_name, coefficients, intercept)
    equation_terms = [f"{coeff:.4f}*{name}" for coeff, name in zip(coefficients, feature_names)]
    equation = " + ".join(equation_terms) + f" + {intercept:.4f}"
    print(f'The equation of the best model for {case_name}: TunnelTemp = {equation}\n')


def write_coefficients_to_file(case_name, coefficients, intercept):
    # Convert coefficients and intercept into a list
    coeffs_list = list(coefficients) + [intercept]

    # Get the current date and time
    current_datetime = datetime.datetime.now()

    # Format the date and time into a string
    datetime_str = current_datetime.strftime("%Y%m%d-%H%M%S")

    # Create the filename with the current date and time
    filename = f"{case_name}Slow-{datetime_str}.txt"

    # Open the file and append the data
    with open(filename, "a") as file:
        file.write(f"'{case_name}': {coeffs_list},\n")


# Train and print the model for each case
train_and_print_equation(data_case_1, "eq1")
train_and_print_equation(data_case_2, "eq2")
train_and_print_equation(data_case_3, "eq3")
