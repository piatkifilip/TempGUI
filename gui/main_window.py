# gui/main_window.py

import tkinter as tk
from tkinter import filedialog
from gui.coefficients import create_coefficient_inputs
from gui.plot_window import initialize_plot_window, update_plot
from gui.data_processing import load_and_process_data
from models.equations import default_coeffs
from .data_processing import calculate_mea
from .statistics_window import StatisticsWindow
current_sheet_index = 0

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.excel_path = 'data/3C.xlsx'  # Set the default Excel file path here
        self.coefficients_inputs = {}
        self.setup_ui()
        self.plot_window, self.fig, self.canvas = initialize_plot_window(root)
        self.stats_window = StatisticsWindow(self.root)
        self.on_update_plot()  # Load and process the default Excel file
        self.stats_window = StatisticsWindow(self.root)
        prev_button = tk.Button(self, text="Previous", command=self.prev_file)
        prev_button.pack(side=tk.LEFT)

        next_button = tk.Button(self, text="Next", command=self.next_file)
        next_button.pack(side=tk.RIGHT)

    def setup_ui(self):
        self.root.title("Input Coefficients")
        frame_controls = tk.Frame(self.root)
        frame_controls.grid(row=0, column=0, sticky="nsew")

        # Coefficient inputs
        for eq_label, default_values in default_coeffs.items():
            frame = tk.Frame(frame_controls)
            frame.pack(fill=tk.X)
            self.coefficients_inputs[eq_label] = create_coefficient_inputs(frame, eq_label, default_values)

        # Buttons
        button_load_excel = tk.Button(frame_controls, text="Load Excel File", command=self.on_load_excel_file)
        button_load_excel.pack(side=tk.LEFT)
        button_update_plot = tk.Button(frame_controls, text="Update Plot", command=self.on_update_plot)
        button_update_plot.pack(side=tk.LEFT)

        frame_controls.pack()

    def on_load_excel_file(self):
        self.excel_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        if self.excel_path:
            self.on_update_plot()

    def on_update_plot(self):
        coeffs = {
            eq: [float(entry.get()) for entry in entries]
            for eq, entries in self.coefficients_inputs.items()
        }
        if self.excel_path:
            data_sheets = load_and_process_data(self.excel_path, coeffs)
            update_plot(data_sheets, self.fig, self.canvas)
        stats_text = ""  # Initialize an empty string to collect all MEA stats
        for file_name, sheet_name, data in data_sheets:
            mea1 = calculate_mea(data, (35, 65), 'Predicted_TunnelTemp')
            mea2 = calculate_mea(data, (52, 63), 'Predicted_TunnelTemp')
            stats_text += f"Sheet '{sheet_name}' MEA 35-65°C: {mea1}\n          MEA 52-63°C: {mea2}"
            self.stats_window.update_statistics(stats_text)

    def next_file():
        global current_file_index
        global data_sheets
        global fig
        global canvas

        current_file_index = (current_file_index + 1) % len(data_sheets)
        update_plot(data_sheets, fig, canvas)

    # Function to handle the 'Previous' button click
    def prev_file():
        global current_file_index
        global data_sheets
        global fig
        global canvas

        current_file_index = (current_file_index - 1) % len(data_sheets)
        update_plot(data_sheets, fig, canvas)
