import tkinter as tk
current_sheet_index = 0

class StatisticsWindow:
    def __init__(self, master):
        self.master = master
        self.stats_win = tk.Toplevel(self.master)
        self.stats_win.title("MEA Statistics")
        self.text_widget = tk.Text(self.stats_win, wrap='word', height=30, width=80)
        self.text_widget.pack()

    def update_statistics(self, stats_text):
        self.text_widget.delete(1.0, tk.END)  # Clear the previous statistics
        self.text_widget.insert(tk.END, stats_text)