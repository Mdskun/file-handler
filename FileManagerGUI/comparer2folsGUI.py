#This program compares two folder graphically and delete 
import tkinter as tk
from tkinter import messagebox, filedialog
import os

# Function to load the contents of the first directory into the first listbox
def load_directory1():
    folder1 = filedialog.askdirectory(title="Select First Folder")
    if folder1:
        listbox1.delete(0, tk.END)
        for item in os.listdir(folder1):
            listbox1.insert(tk.END, os.path.join(folder1, item))

# Function to load the contents of the second directory into the second listbox
def load_directory2():
    folder2 = filedialog.askdirectory(title="Select Second Folder")
    if folder2:
        listbox2.delete(0, tk.END)
        for item in os.listdir(folder2):
            listbox2.insert(tk.END, os.path.join(folder2, item))

# Function to delete selected files from the listbox
def delete_selected_files(listbox):
    selected_items = listbox.curselection()
    for item in selected_items[::-1]:  # Reverse the selection order to avoid index shifting
        file_path = listbox.get(item)
        try:
            os.remove(file_path)
            listbox.delete(item)
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting {file_path}: {e}")

# Create the main window
root = tk.Tk()
root.title("Folder Viewer and File Deleter")

# Create frames for each folder
frame1 = tk.Frame(root)
frame2 = tk.Frame(root)

frame1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
frame2.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Create listboxes for each folder
listbox1 = tk.Listbox(frame1, selectmode=tk.MULTIPLE, width=50, height=30)
listbox2 = tk.Listbox(frame2, selectmode=tk.MULTIPLE, width=50, height=30)

listbox1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
listbox2.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Create scrollbars for each listbox
scrollbar1 = tk.Scrollbar(frame1, orient=tk.VERTICAL, command=listbox1.yview)
scrollbar2 = tk.Scrollbar(frame2, orient=tk.VERTICAL, command=listbox2.yview)

scrollbar1.pack(side=tk.RIGHT, fill=tk.Y)
scrollbar2.pack(side=tk.RIGHT, fill=tk.Y)

listbox1.config(yscrollcommand=scrollbar1.set)
listbox2.config(yscrollcommand=scrollbar2.set)

# Create buttons to load directories and delete files
load_button1 = tk.Button(root, text="Load First Directory", command=load_directory1)
load_button2 = tk.Button(root, text="Load Second Directory", command=load_directory2)
delete_button1 = tk.Button(root, text="Delete Selected Files from Folder 1", command=lambda: delete_selected_files(listbox1))
delete_button2 = tk.Button(root, text="Delete Selected Files from Folder 2", command=lambda: delete_selected_files(listbox2))

load_button1.pack(side=tk.TOP, fill=tk.X)
load_button2.pack(side=tk.TOP, fill=tk.X)
delete_button1.pack(side=tk.LEFT, fill=tk.X)
delete_button2.pack(side=tk.RIGHT, fill=tk.X)

# Run the main loop
root.mainloop()
