import shutil
import re
import os

print("This program moves file by certain extentions")

def move_all(type,source,destination):
    list_of_files=os.listdir(source)
    for ma in list_of_files:
        match=re.search(r"\."+type,str(ma))
        if match:
            shutil.move(source+"/"+ma,destination)

def move_cetrtain_files_with_subdir(type,source,destination):
    for root, dirs, files in os.walk(source):
        for filename in files:
            if filename.endswith(type):
                source_path = os.path.join(root,filename)
                destination_path = os.path.join(destination,filename)

                #to copy folder this things are commented down

                #relative_path = os.path.relpath(source_path,source)
                #destination_path = os.path.join(destination,relative_path)
                #os.makedirs(os.path.dirname(destination_path),exist_ok=True)

                shutil.move(source_path, destination_path)
                print(f"Moved '{source_path}' to '{destination_path}'")

#move_cetrtain_files_with_subdir(".mp3","E:/mom","F:/music")