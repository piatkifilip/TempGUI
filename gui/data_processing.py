# gui/data_processing.py
import os
import pandas as pd
import numpy as np
from tkinter import messagebox
from models.equations import terms, default_coeffs, current_equation_set
from sklearn.metrics import mean_absolute_error

def predict_tunnel_temp(row, coeffs, current_equation_set):
    delta = row['delta']
    if current_equation_set == 1:
        equation_used = 'eq1' if delta > 3 else 'eq2' if -3 <= delta <= 3 else 'eq3'
    else:  # current_equation_set == 2
        equation_used = 'eq4' if delta > 3 else 'eq5' if -3 <= delta <= 3 else 'eq6'

    predicted_temp = np.dot(coeffs[equation_used], [
        row['HeadTemp1'], row['HeadTemp2'], row['Slope_HeadTemp1'],
        row['Slope_HeadTemp2'], row['Ratio_HeadTemp1_HeadTemp2'], 1
    ])
    return predicted_temp, equation_used

def load_and_process_data(excel_path, coeffs, current_equation_set):
    try:
        xls = pd.ExcelFile(excel_path)
        data_sheets = []
        file_name = os.path.basename(excel_path)
        for sheet_name in xls.sheet_names:
            df = xls.parse(sheet_name)
            df['Slope_HeadTemp1'] = df['HeadTemp1'].diff().fillna(method='bfill')
            df['Slope_HeadTemp2'] = df['HeadTemp2'].diff().fillna(method='bfill')
            df['delta'] = df['HeadTemp1'] - df['HeadTemp2']
            df['Ratio_HeadTemp1_HeadTemp2'] = df['HeadTemp1'].div(df['HeadTemp2'].replace({0: np.nan})).fillna(method='bfill')
            df['Predicted_TunnelTemp'], df['EquationUsed'] = zip(*df.apply(lambda row: predict_tunnel_temp(row, coeffs, current_equation_set), axis=1))

            df['HeadTemp1'] = df['HeadTemp1']
            df['HeadTemp2'] = df ['HeadTemp2']
            data_sheets.append((file_name, sheet_name, df))
        return data_sheets
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while processing the data: {e}")
        return None
def calculate_mea(data, temp_range, predictions, actual='TunnelTemp'):
    mask = (data[actual] >= temp_range[0]) & (data[actual] <= temp_range[1])
    return mean_absolute_error(data.loc[mask, actual], data.loc[mask, predictions])

# Update the load_and_process_data function to also calculate MEA
# This means you'll need to return the MEA values as well and handle these in your main_window.py