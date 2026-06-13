import os

print("This program genarates a file report\n")

def file_report_of(path):                 #This function creates last summery in directory
    d={"mp3":0,"mp4":0,"mvi":0,"jpg":0,"png":0,"pdf":0,"txt":0,"log":0,"word":0,"power point":0,"exel":0,"zip":0,"html":0,"css":0,"javascript":0,"py":0,"java":0}
    # print(path)
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.mp3'):
                d["mp3"]+=1
            elif file.endswith('.mp4'):
                d["mp4"] += 1
            elif file.endswith('.mvi'):
                d["mvi"] += 1
            elif file.endswith(('.jpg','.jpeg')):
                d["jpg"] += 1
            elif file.endswith('.png'):
                d["png"] += 1
            elif file.endswith('.pdf'):
                d["pdf"] += 1
            elif file.endswith(('.docx','.doc')):
                d["word"] += 1
            elif file.endswith(('.ppt', '.pptx')):
                d["power point"] += 1
            elif file.endswith(('.xlsx', '.xls','.csv')):
                d["exel"] += 1
            elif file.endswith('.zip'):
                d["zip"] += 1
            elif file.endswith('.java'):
                d["java"] += 1
            elif file.endswith('.txt'):
                d["txt"] += 1
            elif file.endswith('.log'):
                d["log"] += 1
            elif file.endswith('.html'):
                d["html"] += 1
            elif file.endswith('.css'):
                d["css"] += 1
            elif file.endswith('.js'):
                d["javascript"] += 1
            elif file.endswith('.py'):
                d["py"] += 1
            #elif file.endswith('.py'):
                #d["py"] += 1
    return d

def generate_directory_tree(folder_path, file, prefix="", exclude_folders=None):
    """Recursively generate directory tree with dotted structure, excluding specified folders."""
    if exclude_folders is None:
        exclude_folders = []
        
    items = sorted(os.listdir(folder_path))  # List all files and directories in the current folder
    
    for index, item in enumerate(items):
        item_path = os.path.join(folder_path, item)
        
        # If the item is a directory and in the exclude_folders list, skip it
        if any(os.path.samefile(item_path, exclude_folder) for exclude_folder in exclude_folders):
            continue
        
        # If it's the last item in the current directory, use a different connector
        is_last_item = (index == len(items) - 1)
        
        # Formatting: └── for the last item, ├── for others
        if is_last_item:
            connector = "└── "
        else:
            connector = "├── "
        
        # Write the item to the file with the proper prefix and connector
        file.write(f"{prefix}{connector}{item}\n")
        
        # If the item is a directory, recursively list its contents
        if os.path.isdir(item_path):
            # Extend the prefix with '│   ' if not last, or '    ' if last
            new_prefix = prefix + ("    " if is_last_item else "│   ")
            generate_directory_tree(item_path, file, new_prefix, exclude_folders)

def save_directory_tree_to_file(folder_path, output_file_path, exclude_folders=None):
    """Saves the directory tree of the given folder into a text file with dotted structure."""
    with open(output_file_path, 'w',encoding='utf-8') as file:
        file.write(f"Directory tree for {folder_path}:\n\n")
        
        # Convert all exclude folders to their absolute paths for consistency
        if exclude_folders:
            exclude_folders = [os.path.abspath(os.path.join(folder_path, exclude_folder.strip())) for exclude_folder in exclude_folders]

        generate_directory_tree(folder_path, file, exclude_folders=exclude_folders)
        report_in_dict=file_report_of(folder_path)
        file.write("\n-------->The summery of above is:-")
        for count in report_in_dict:
            if report_in_dict[count] == 0:
                pass
            else:
                file.write("\n---->There are "+str(report_in_dict[count])+" files of "+count+" type are here")

path=input("please enter the path:-\n")
path=os.path.abspath(path)

exclude_folders_input = input("Enter folders to exclude (comma-separated, leave empty for none): ")
if exclude_folders_input.strip():
    exclude_folders = [os.path.join(path, folder.strip()) for folder in exclude_folders_input.split(",")]
else:
    exclude_folders = []
save_path ="/home/hp/Data/Dump/"
save_file_name="File_repo.txt"
save_directory_tree_to_file(path, save_path+save_file_name, exclude_folders)
print("The report Genarated")