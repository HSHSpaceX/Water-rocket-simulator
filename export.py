import tkinter as tk
from tkinter import ttk

def open_entry_window():
    entry_window = tk.Toplevel(root)
    entry_window.title("Entry Window")

    entry_var = tk.StringVar()
    entry = ttk.Entry(entry_window, textvariable=entry_var)
    entry.pack(padx=10, pady=5)

    ok_button = ttk.Button(entry_window, text="OK", command=lambda: save_and_close(entry_var, entry_window))
    ok_button.pack(pady=10)

def save_and_close(entry_var, window):
    value_entry = entry_var.get()
    label.config(text=value_entry)
    window.destroy()

root = tk.Tk()
root.title("Main Window")

label = ttk.Label(root, text="Label Text")
label.pack(pady=10)

button = ttk.Button(root, text="Open Entry Window", command=open_entry_window)
button.pack(pady=10)

root.mainloop()
