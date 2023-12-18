import tkinter as tk
from tkinter import filedialog

def save_to_file(entry_text):
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(entry_text.get())

def load_from_file(entry_text):
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "r") as file:
            content = file.read()
            entry_text.set(content)

def main():
    root = tk.Tk()
    root.title("File Editor")

    entry_var = tk.StringVar()

    entry = tk.Entry(root, textvariable=entry_var)
    entry.pack(pady=10, padx=10)

    menubar = tk.Menu(root)

    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="Save", command=lambda: save_to_file(entry_var))
    file_menu.add_command(label="Load", command=lambda: load_from_file(entry_var))

    menubar.add_cascade(label="File", menu=file_menu)

    root.config(menu=menubar)

    root.mainloop()

if __name__ == "__main__":
    main()
 