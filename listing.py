import tkinter as tk
from tkinter import ttk

def on_select(event):
    selected_option = combo_var.get()
    selected_label.config(text=f"Selected: {selected_option}")

# Create the main Tkinter window
root = tk.Tk()
root.title("Dropdown Menu App")

# Create a label for displaying the selected option
selected_label = ttk.Label(root, text="Selected: ")
selected_label.pack(pady=10)

# Create a StringVar to hold the selected value from the combobox
combo_var = tk.StringVar()

# Create a combobox (dropdown menu)
options = ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5"]
combobox = ttk.Combobox(root, textvariable=combo_var, values=options, state="readonly")
combobox.pack(pady=10)
combobox.bind("<<ComboboxSelected>>", on_select)

# Run the Tkinter event loop
root.mainloop()
