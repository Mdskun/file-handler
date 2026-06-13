import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

# Function to browse for a directory
def browse_directory():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        folder_path.set(folder_selected)
        scan_files()

# Function to scan for mp3 files in the directory
def scan_files():
    folder = folder_path.get()
    mp3_files.clear()
    if os.path.isdir(folder):
        for file in os.listdir(folder):
            if file.endswith(".mp3"):
                mp3_files.append(file)
        if mp3_files:
            current_file.set(mp3_files[0])
        else:
            messagebox.showinfo("No Files", "No mp3 files found in the selected directory.")
    else:
        messagebox.showerror("Error", "Selected path is not a directory.")

# Function to move file to the selected folder
def move_file(destination_folder):
    src_folder = folder_path.get()
    dest_folder = os.path.join(src_folder, destination_folder)
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    
    current = current_file.get()
    if current:
        shutil.move(os.path.join(src_folder, current), os.path.join(dest_folder, current))
        mp3_files.remove(current)
        if mp3_files:
            current_file.set(mp3_files[0])
        else:
            current_file.set("")
            messagebox.showinfo("Done", "All files have been moved.")

# Function to delete the current file
def delete_file():
    src_folder = folder_path.get()
    current = current_file.get()
    if current:
        os.remove(os.path.join(src_folder, current))
        mp3_files.remove(current)
        if mp3_files:
            current_file.set(mp3_files[0])
        else:
            current_file.set("")
            messagebox.showinfo("Done", "All files have been processed.")

# Setting up the GUI
root = tk.Tk()
root.title("MP3 File Mover")

folder_path = tk.StringVar()
current_file = tk.StringVar()
mp3_files = []

frame = tk.Frame(root)
frame.pack(pady=10)

browse_button = tk.Button(frame, text="Browse", command=browse_directory)
browse_button.pack(side=tk.LEFT, padx=5)

folder_entry = tk.Entry(frame, textvariable=folder_path, width=50)
folder_entry.pack(side=tk.LEFT, padx=5)

file_label = tk.Label(root, textvariable=current_file)
file_label.pack(pady=10)

buttons_frame = tk.Frame(root)
buttons_frame.pack(pady=10)

folder1_button = tk.Button(buttons_frame, text="Folder1", command=lambda: move_file("Folder1"))
folder1_button.pack(side=tk.LEFT, padx=5)

folder2_button = tk.Button(buttons_frame, text="Folder2", command=lambda: move_file("Folder2"))
folder2_button.pack(side=tk.LEFT, padx=5)

folder3_button = tk.Button(buttons_frame, text="Folder3", command=lambda: move_file("Folder3"))
folder3_button.pack(side=tk.LEFT, padx=5)

delete_button = tk.Button(buttons_frame, text="Delete", command=delete_file)
delete_button.pack(side=tk.LEFT, padx=5)

root.mainloop()
