import tkinter as tk

class StatisticsWindow:
    def __init__(self, master):
        self.master = master
        self.stats_win = tk.Toplevel(self.master)
        self.stats_win.title("MEA Statistics")
        self.text_widget = tk.Text(self.stats_win, wrap='word', height=50, width=80)
        self.text_widget.pack()
        self.clear_button = tk.Button(self.stats_win, text="Clear", command=self.clear_text)
        self.clear_button.pack()

    def update_statistics(self, stats_text):
        # Insert the new stats at the end of the text widget, followed by a newline for separation
        self.text_widget.insert(tk.END, stats_text + '\n\n')  # Adding an extra newline for better separation
        self.text_widget.see(tk.END)  # Auto-scroll to the end

    def clear_text(self):
        self.text_widget.delete(1.0, tk.END)