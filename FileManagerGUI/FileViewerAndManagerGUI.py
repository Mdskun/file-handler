import tkinter as tk
from tkinter import filedialog, messagebox
import shutil
import os

class FileManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Manager")
        self.root.geometry("600x450")  # Increased height to accommodate status bar

        self.folder_path = tk.StringVar()
        
        # Folder selection
        self.folder_label = tk.Label(root, text="Folder Path:")
        self.folder_label.pack(pady=5)
        self.folder_entry = tk.Entry(root, textvariable=self.folder_path, width=50)
        self.folder_entry.pack(pady=5)
        self.browse_button = tk.Button(root, text="Browse", command=self.browse_folder)
        self.browse_button.pack(pady=5)

        # File list with scrollbar
        self.file_frame = tk.Frame(root)
        self.file_frame.pack(pady=10)

        self.file_scrollbar = tk.Scrollbar(self.file_frame, orient=tk.VERTICAL)
        self.file_listbox = tk.Listbox(self.file_frame, selectmode=tk.MULTIPLE, width=80, height=15, yscrollcommand=self.file_scrollbar.set)
        self.file_scrollbar.config(command=self.file_listbox.yview)
        self.file_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.file_listbox.bind('<<ListboxSelect>>', self.update_status_bar)  # Bind selection event to update status bar

        # Operation buttons
        self.copy_button = tk.Button(root, text="Copy", command=self.copy_files)
        self.copy_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.move_button = tk.Button(root, text="Move", command=self.move_files)
        self.move_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.delete_button = tk.Button(root, text="Delete", command=self.delete_files)
        self.delete_button.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Status bar
        self.status_bar = tk.Label(root, text="No files selected", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.folder_path.set(folder_selected)
            self.update_file_list()
            self.update_status_bar()  # Update status bar when folder changes

    def update_file_list(self):
        self.file_listbox.delete(0, tk.END)
        folder = self.folder_path.get()
        try:
            files = os.listdir(folder)
            files.sort()  # Sort files alphabetically
            for file in files:
                self.file_listbox.insert(tk.END, file)
        except Exception as e:
            messagebox.showerror("Error", f"Could not list files in the folder: {str(e)}")
        
    def update_status_bar(self, event=None):
        selected_files = len(self.file_listbox.curselection())
        self.status_bar.config(text=f"{selected_files} files selected")

    def copy_files(self):
        selected_files = self.get_selected_files()
        if not selected_files:
            return
        
        destination_folder = filedialog.askdirectory()
        if not destination_folder:
            return
        
        for file in selected_files:
            source_path = os.path.join(self.folder_path.get(), file)
            destination_path = os.path.join(destination_folder, file)
            try:
                shutil.copy2(source_path, destination_path)
            except Exception as e:
                messagebox.showerror("Error", f"Could not copy {file}: {str(e)}")
        
        messagebox.showinfo("Success", "Selected files copied successfully.")
        self.update_status_bar()

    def move_files(self):
        selected_files = self.get_selected_files()
        if not selected_files:
            return
        
        destination_folder = filedialog.askdirectory()
        if not destination_folder:
            return
        
        for file in selected_files:
            source_path = os.path.join(self.folder_path.get(), file)
            destination_path = os.path.join(destination_folder, file)
            try:
                shutil.move(source_path, destination_path)
            except Exception as e:
                messagebox.showerror("Error", f"Could not move {file}: {str(e)}")
        
        self.update_file_list()
        messagebox.showinfo("Success", "Selected files moved successfully.")
        self.update_status_bar()

    def delete_files(self):
        selected_files = self.get_selected_files()
        if not selected_files:
            return
        
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected files?")
        if not confirm:
            return
        
        for file in selected_files:
            file_path = os.path.join(self.folder_path.get(), file)
            try:
                os.remove(file_path)
            except Exception as e:
                messagebox.showerror("Error", f"Could not delete {file}: {str(e)}")
        
        self.update_file_list()
        messagebox.showinfo("Success", "Selected files deleted successfully.")
        self.update_status_bar()
    
    def get_selected_files(self):
        selected_indices = self.file_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("No Selection", "Please select one or more files.")
            return []
        
        return [self.file_listbox.get(i) for i in selected_indices]

if __name__ == "__main__":
    root = tk.Tk()
    app = FileManagerApp(root)
    root.mainloop()
