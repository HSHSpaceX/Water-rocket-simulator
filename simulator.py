import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

def plot_graph():
    try:
        # Retrieve the value from the entry widget
        x_value = float(entry_0.get())

        # Generate some example data for the plot
        y_values = [x_value ** 2, x_value ** 3, x_value ** 4]

        # Clear the previous plot
        ax.clear()

        # Plot the new data
        ax.plot([2, 3, 4], y_values, marker='o', linestyle='-', color='b')

        # Set labels and title
        ax.set_xlabel('X-axis')
        ax.set_ylabel('Y-axis')
        ax.set_title('Graph of DUPA')

        # Update the canvas
        canvas.draw()

    except ValueError:
        # Handle the case where the entered value is not a valid float
        error_label.config(text="Invalid input. Please enter a numeric value.")

# Create the main Tkinter window
root = tk.Tk()
root.title("Water Rocket Simulator")

# Create and pack widgets on the left side
frame_left = ttk.Frame(root, padding="10")
frame_left.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

label_0 = ttk.Label(frame_left, text="Enter pressure value:")
label_0.grid(row=0, column=0, columnspan=2, pady=5, sticky="w")

entry_0 = ttk.Entry(frame_left, width=10)
entry_0.grid(row=0, column=2, pady=5)
entry_0.insert(0, "0")  # Initialize with a default value

label_1 = ttk.Label(frame_left, text="Enter area throat value:")
label_1.grid(row=1, column=0, columnspan=2, pady=5, sticky="w")

entry_1 = ttk.Entry(frame_left, width=10)
entry_1.grid(row=1, column=2, pady=5)
entry_1.insert(0, "0")  # Initialize with a default value

label_2 = ttk.Label(frame_left, text="Enter air volume value:")
label_2.grid(row=2, column=0, columnspan=2,  pady=5, sticky="w")

entry_2 = ttk.Entry(frame_left, width=10)
entry_2.grid(row=2, column=2, pady=5)
entry_2.insert(0, "0")  # Initialize with a default value

label_3 = ttk.Label(frame_left, text="Enter water volume value:")
label_3.grid(row=3, column=0, columnspan=2, pady=5, sticky="w")

entry_3 = ttk.Entry(frame_left, width=10)
entry_3.grid(row=3, column=2, pady=5)
entry_3.insert(0, "0")  # Initialize with a default value


label_4 = ttk.Label(frame_left, text="Enter mass of rocket value:")
label_4.grid(row=4, column=0, columnspan=2, pady=5, sticky="w")

entry_4 = ttk.Entry(frame_left, width=10)
entry_4.grid(row=4, column=2, pady=5)
entry_4.insert(0, "0")  # Initialize with a default value

plot_button = ttk.Button(frame_left, text="Plot", command=plot_graph)
plot_button.grid(row=5, column=0, columnspan=2, pady=10)

error_label = ttk.Label(frame_left, text="", foreground="red")
error_label.grid(row=6, column=0, columnspan=2, pady=5)

# Create a Matplotlib figure and a canvas to embed it in the Tkinter window
fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))

# Run the Tkinter event loop
root.mainloop()

