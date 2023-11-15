import tkinter as tk
from tkinter import ttk

class StatisticsWindow:
    def __init__(self, master, title="Statistics"):
        self.master = master
        self.stats_win = tk.Toplevel(self.master)
        self.stats_win.title(title)

        self.tree = ttk.Treeview(self.stats_win, columns=('Orientation', 'MEA 35-65 °C', 'MEA 57°C'), show='headings')
        self.tree.heading('Orientation', text='Orientation')
        self.tree.heading('MEA 35-65 °C', text='MEA 35-65 °C')
        self.tree.heading('MEA 57°C', text='MEA 57°C')
        self.tree.pack(expand=True, fill='both')
        # Assuming you have a treeview named `self.tree`
        self.tree.column("#2", anchor="center")
        self.tree.column("#3", anchor="center")

    def update_statistics(self, sheet_name, mea1, mea2):
        # Round the values to 3 decimal places
        mea1_rounded = round(mea1, 3)
        mea2_rounded = round(mea2, 3)

        # Insert the rounded values into the treeview
        self.tree.insert('', 'end', values=(sheet_name, mea1_rounded, mea2_rounded))