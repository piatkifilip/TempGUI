# gui/main_window.py

import tkinter as tk
from tkinter import filedialog
from gui.coefficients import create_coefficient_inputs
from gui.coefficients import  CoefficientsWindow
from gui.plot_window import initialize_plot_window, update_plot
from gui.data_processing import load_and_process_data
from models.equations import default_coeffs
from .data_processing import calculate_mea
from .statistics_window import StatisticsWindow


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.excel_path = 'data/30C-16.xlsx'  # Set the default Excel file path here
        self.coefficients_inputs = {}
        self.coefficients_window = CoefficientsWindow(self.root, self)
        self.setup_ui()
        self.plot_window, self.fig, self.canvas = initialize_plot_window(root)
        self.stats_window = StatisticsWindow(self.root)
        self.on_update_plot()  # Load and process the default Excel file
        self.stats_window = StatisticsWindow(self.root)

    def setup_ui(self):
        self.root.title("Input Coefficients")
        frame_controls = tk.Frame(self.root)
        frame_controls.pack(fill=tk.X, expand=True)


        # Buttons
        button_frame = tk.Frame(frame_controls)
        button_frame.pack(fill=tk.X)
        button_load_excel = tk.Button(button_frame, text="Load Excel File", command=self.on_load_excel_file)
        button_load_excel.pack(side=tk.LEFT)
        button_update_plot = tk.Button(button_frame, text="Update Plot", command=self.on_update_plot)
        button_update_plot.pack(side=tk.LEFT)

        frame_controls.pack()

    def on_load_excel_file(self):
        self.excel_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        if self.excel_path:
            self.on_update_plot()

    def on_update_plot(self):
        global current_equation_set
        current_equation_set = self.coefficients_window.eq_set_var.get()
        coeffs = self.coefficients_window.get_coefficients()

        print("Coefficients:", coeffs)
        print("Current Equation Set:", current_equation_set)

        if self.excel_path:
            data_sheets = load_and_process_data(self.excel_path, coeffs, current_equation_set)  # Pass current_set
            update_plot(data_sheets, self.fig, self.canvas)

        stats_text = ""  # Initialize an empty string to collect all MEA stats
        for file_name, sheet_name, data in data_sheets:
            mea1 = calculate_mea(data, (35, 65), 'Predicted_TunnelTemp')
            mea2 = calculate_mea(data, (52, 63), 'Predicted_TunnelTemp')
            stats_text = f"Sheet '{sheet_name}' MEA 35-65°C: {mea1}\n          MEA 52-63°C: {mea2}"
            self.stats_window.update_statistics(stats_text)

    def refresh_plot(self):
        self.on_update_plot()