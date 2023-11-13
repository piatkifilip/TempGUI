# gui/main_window.py

import tkinter as tk
from tkinter import filedialog
from gui.coefficients import create_coefficient_inputs
from gui.plot_window import initialize_plot_window, update_plot
from gui.data_processing import load_and_process_data
from models.equations import default_coeffs


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.excel_path = ''
        self.coefficients_inputs = {}
        self.setup_ui()
        self.plot_window, self.fig, self.canvas = initialize_plot_window(root)

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
