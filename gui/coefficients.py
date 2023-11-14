# gui/coefficients.py

import tkinter as tk
from tkinter import filedialog
import ast
from models.equations import terms, default_coeffs, current_equation_set
selected_set = 1

class CoefficientsWindow:
    def __init__(self, master, main_window):
        self.master = master
        self.main_window = main_window
        self.setup_ui()
        self.main_window.coefficients_window = self
    def setup_ui(self):
        # Checkbutton for selecting equation set
        self.eq_set_var = tk.IntVar(value=selected_set)
        self.eq_set_checkbutton = tk.Checkbutton(self.master, text="Equation 1, 2, 3", variable=self.eq_set_var, command=self.toggle_equation_set)
        self.eq_set_checkbutton.pack()

        self.nrows_var = tk.IntVar(value=4)
        self.ncols_var = tk.IntVar(value=4)
        self.setup_scroll_inputs()

        # Main frame for coefficients
        coeffs_main_frame = tk.Frame(self.master)
        coeffs_main_frame.pack(fill=tk.X)

        # Frame for coefficients 1-3
        coeffs_1_3_frame = tk.Frame(coeffs_main_frame)
        coeffs_1_3_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Frame for coefficients 4-6
        coeffs_4_6_frame = tk.Frame(coeffs_main_frame)
        coeffs_4_6_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Coefficient inputs
        self.coefficient_frames = {}
        for eq_label, default_values in default_coeffs.items():
            frame = coeffs_1_3_frame if eq_label in ['eq1', 'eq2', 'eq3'] else coeffs_4_6_frame
            frame_pack = tk.Frame(frame)
            frame_pack.pack(fill=tk.X)
            self.coefficient_frames[eq_label] = create_coefficient_inputs(frame_pack, eq_label, default_values)

    def setup_scroll_inputs(self):
        nrows_spinbox = tk.Spinbox(self.master, from_=1, to=10, textvariable=self.nrows_var)
        nrows_spinbox.pack()
        ncols_spinbox = tk.Spinbox(self.master, from_=1, to=10, textvariable=self.ncols_var)
        ncols_spinbox.pack()

    def load_set_1(self):
        self.load_coefficients(set_number=1)

    def load_set_2(self):
        self.load_coefficients(set_number=2)

    def load_coefficients(self, set_number):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                new_coeffs = ast.literal_eval(f"{{{content}}}")
                self.update_coefficients(new_coeffs, set_number)


    def update_coefficients(self, new_coeffs, set_number):
        # Assuming new_coeffs is a dictionary with keys as equation labels
        for eq_label, coeffs in new_coeffs.items():
            if set_number == 1 and eq_label in ['eq1', 'eq2', 'eq3'] or \
                    set_number == 2 and eq_label in ['eq4', 'eq5', 'eq6']:
                entries = self.coefficient_frames[eq_label]
                for i, entry in enumerate(entries):
                    entry.delete(0, tk.END)
                    entry.insert(0, str(coeffs[i]))

    def toggle_equation_set(self):
        global selected_set
        selected_set = self.eq_set_var.get()
        self.update_coefficient_inputs()

    def update_coefficient_inputs(self):
        global selected_set
        selected_set = self.eq_set_var.get()
        for eq_label, frame in self.coefficient_frames.items():
            # Clear existing widgets in the frame
            for widget in frame.winfo_children():
                widget.destroy()

            # Create new inputs
            new_default_values = default_coeffs[eq_label] if selected_set == 1 else default_coeffs[
                f'eq{eq_label[-1]}_set2']
            self.coefficient_frames[eq_label] = create_coefficient_inputs(frame, eq_label, new_default_values)

    def get_coefficients(self):
        coeffs = {}
        for eq_label, entries in self.coefficient_frames.items():
            coeffs[eq_label] = [float(entry.get()) for entry in entries]
        return coeffs

def create_coefficient_inputs(frame, eq_label, default_values):
    entries = []
    for index, (term, value) in enumerate(zip(terms[eq_label], default_values)):
        term_label = tk.Label(frame, text=f"{term}:")
        term_label.grid(row=index, column=0, sticky="ew")
        entry = tk.Entry(frame)
        entry.grid(row=index, column=1, sticky="ew", padx=5)
        entry.insert(0, str(value))  # Set default coefficient value
        entries.append(entry)
        frame.grid_columnconfigure(1, weight=1)
    return entries
