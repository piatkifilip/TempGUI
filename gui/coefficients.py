# gui/coefficients.py

import tkinter as tk
from models.equations import terms
current_sheet_index = 0

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
