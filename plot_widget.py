import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np

def plot_left_graph():
    x = np.linspace(0, 2 * np.pi, 100)
    y = np.sin(x)

    ax_left.clear()
    ax_left.plot(x, y, marker='o', linestyle='-', color='b')
    ax_left.set_xlabel('X-axis')
    ax_left.set_ylabel('Y-axis')
    ax_left.set_title('Left Sine Wave')
    canvas_left.draw()

def plot_right_graph():
    x = np.linspace(0, 2 * np.pi, 100)
    y = np.cos(x)

    ax_right.clear()
    ax_right.plot(x, y, marker='o', linestyle='-', color='r')
    ax_right.set_xlabel('X-axis')
    ax_right.set_ylabel('Y-axis')
    ax_right.set_title('Right Cosine Wave')
    canvas_right.draw()

root = tk.Tk()
root.title("Resizable Dual Plots")

# Set the window size to full screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")

# Configure grid weights for resizing
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=0)  # No weight for the separator
root.columnconfigure(2, weight=1)
root.rowconfigure(0, weight=1)

# Left plot
frame_left = ttk.Frame(root, padding="10")
frame_left.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

fig_left, ax_left = plt.subplots(figsize=(screen_width / 200, screen_height / 120))
canvas_left = FigureCanvasTkAgg(fig_left, master=frame_left)
canvas_widget_left = canvas_left.get_tk_widget()
canvas_widget_left.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

plot_button_left = ttk.Button(frame_left, text="Plot Left", command=plot_left_graph)
plot_button_left.grid(row=1, column=0, pady=10)

# Right plot
frame_right = ttk.Frame(root, padding="10")
frame_right.grid(row=0, column=2, sticky=(tk.W, tk.E, tk.N, tk.S))

fig_right, ax_right = plt.subplots(figsize=(screen_width / 200, screen_height / 100))
canvas_right = FigureCanvasTkAgg(fig_right, master=frame_right)
canvas_widget_right = canvas_right.get_tk_widget()
canvas_widget_right.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

plot_button_right = ttk.Button(frame_right, text="Plot Right", command=plot_right_graph)
plot_button_right.grid(row=1, column=0, pady=10)

# Initialize the plots
plot_left_graph()
plot_right_graph()

# Run the Tkinter event loop
root.mainloop()
