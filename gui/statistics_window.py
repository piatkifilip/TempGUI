import tkinter as tk
from tkinter import ttk

class StatisticsWindow:
    def __init__(self, master):
        self.master = master
        self.stats_win = tk.Toplevel(self.master)
        self.stats_win.title("MEA Statistics")

        self.tree = ttk.Treeview(self.stats_win, columns=('MEA 35-65 °C', 'MEA 52-63°C'), show='headings')
        self.tree.heading('MEA 35-65 °C', text='MEA 35-65 °C')
        self.tree.heading('MEA 52-63°C', text='MEA 52-63°C')
        self.tree.pack(expand=True, fill='both')

    def update_statistics(self, sheet_name, mea1, mea2):
        self.tree.insert('', 'end', values=(sheet_name, mea1, mea2))
