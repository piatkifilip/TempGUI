# gui/plot_window.py

import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox
global data_sheets
current_sheet_index = 0  # This should also be a global variable

def create_plot_window(root):
    plot_window = tk.Toplevel(root)
    plot_window.title("Plots")

    frame_plot = tk.Frame(plot_window)
    frame_plot.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    button_prev = tk.Button(plot_window, text="Previous", command=prev_plot)
    button_prev.pack(side=tk.LEFT)
    button_next = tk.Button(plot_window, text="Next", command=next_plot)
    button_next.pack(side=tk.RIGHT)

    return plot_window, frame_plot

# Functions to handle navigation
current_sheet_index = 0  # Keep track of the current sheet being displayed

def prev_plot():
    global current_sheet_index
    current_sheet_index = max(0, current_sheet_index - 1)
    update_plot()

def next_plot():
    global current_sheet_index
    current_sheet_index = min(len(data_sheets) - 1, current_sheet_index + 1)
    update_plot()

def update_plot(data_sheets, fig, canvas):
    global current_file_index

    if data_sheets:
        # Clear the current figure
        fig.clf()

        # Get the data for the current file
        file_name, sheet_name, data = data_sheets[current_file_index]

        nrows, ncols = 4, 2  # Grid size for subplots
        for i in range(1, nrows * ncols + 1):
            ax = fig.add_subplot(nrows, ncols, i)
            # Assuming 'TunnelTemp' and 'Predicted_TunnelTemp' are columns in your DataFrame
            # and you want to plot them in each subplot
            ax.plot(data['TunnelTemp'], label='Actual TunnelTemp', color='purple')
            unique_eqs = data['EquationUsed'].dropna().unique()
            eq_label = ', '.join(unique_eqs)
            ax.plot(data.index, data['Predicted_TunnelTemp'], label=f'Predicted TunnelTemp ({eq_label})', color='red', linestyle='--')
            ax.set_title(f'{file_name} - {sheet_name}')
            ax.set_xlabel('Time Index')
            ax.set_ylabel('Temperature (°C)')
            ax.legend(loc='upper right', fontsize='small', fancybox=True, framealpha=0.5)

        # Adjust layout to prevent overlap
        fig.tight_layout()

        # Redraw the canvas with the new plot
        canvas.draw()
    else:
        messagebox.showinfo("Info", "No data to plot. Please ensure the Excel file is loaded and processed correctly.")

# Function to handle the 'Next' button click

def initialize_plot_window(root):
    plot_window, frame_plot = create_plot_window(root)
    fig = Figure(figsize=(10, 8))
    canvas = FigureCanvasTkAgg(fig, master=frame_plot)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    return plot_window, fig, canvas
