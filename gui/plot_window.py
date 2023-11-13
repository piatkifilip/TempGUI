# gui/plot_window.py

import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox

def create_plot_window(root):
    plot_window = tk.Toplevel(root)
    plot_window.title("Plots")

    frame_plot = tk.Frame(plot_window)
    frame_plot.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    return plot_window, frame_plot

def update_plot(data_sheets, fig, canvas):
    if data_sheets:
        fig.clf()
        nrows, ncols = 4, 2  # Adjust as needed for the number of sheets
        for i, (file_name, sheet_name, data) in enumerate(data_sheets, start=1):
            ax = fig.add_subplot(nrows, ncols, i)
            ax.plot(data['TunnelTemp'], label='Actual TunnelTemp', color='purple')
            unique_eqs = data['EquationUsed'].dropna().unique()
            eq_label = ', '.join(unique_eqs)
            ax.plot(data.index, data['Predicted_TunnelTemp'], label=f'Predicted TunnelTemp ({eq_label})', color='red', linestyle='--')
            ax.set_title(f'{file_name} - {sheet_name}')
            ax.set_xlabel('Time Index')
            ax.set_ylabel('Temperature (°C)')
            ax.legend(loc='upper right', fontsize='small', fancybox=True, framealpha=0.5)
        fig.tight_layout()
        canvas.draw()
    else:
        messagebox.showinfo("Info", "No data to plot. Please ensure the Excel file is loaded and processed correctly.")

def initialize_plot_window(root):
    plot_window, frame_plot = create_plot_window(root)
    fig = Figure(figsize=(12, 8))
    canvas = FigureCanvasTkAgg(fig, master=frame_plot)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    return plot_window, fig, canvas
