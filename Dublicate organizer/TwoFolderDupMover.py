#this function compares 2 folders and moves same files into "The common" folder & then log actions
import os
import shutil
import hashlib

print("This program moves dublicates to another folder\n")

def get_file_hash(file_path):
    """Compute the SHA256 hash of the file."""
    hash_algo = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_algo.update(chunk)
    return hash_algo.hexdigest()

def find_common_files(folder1, folder2):
    """Find common files in two folders based on file content."""
    folder1_files = {}
    folder2_files = {}
    # Compute hashes for all files in folder1
    for root, _, files in os.walk(folder1):
        for file in files:
            if file.endswith('.mp3'):
                file_path = os.path.join(root, file)
                file_hash = get_file_hash(file_path)
                folder1_files[file_hash] = file_path
    # Compute hashes for all files in folder2
    for root, _, files in os.walk(folder2):
        for file in files:
            if file.endswith('.mp3'):
                file_path = os.path.join(root, file)
                file_hash = get_file_hash(file_path)
                folder2_files[file_hash] = file_path
    # Find common hashes
    common_hashes = set(folder1_files.keys()) & set(folder2_files.keys())
    return common_hashes, folder1_files, folder2_files

def move_common_files(common_hashes, folder1_files, folder2_files, common_folder):
    """Move common files to 'The common' folder and log the actions."""
    if not os.path.exists(common_folder):
        os.makedirs(common_folder)

    moved_files = []

    for file_hash in common_hashes:
        file_path1 = folder1_files[file_hash]
        file_path2 = folder2_files[file_hash]
        # Move files to common folder
        common_file_path = os.path.join(common_folder, os.path.basename(file_path1))
        if not os.path.exists(common_file_path):
            shutil.move(file_path1, common_file_path)
            moved_files.append(file_path1)
        else:
            os.remove(file_path1)
            moved_files.append(file_path1 + " (deleted duplicate)")

        common_file_path = os.path.join(common_folder, os.path.basename(file_path2))
        if not os.path.exists(common_file_path):
            shutil.move(file_path2, common_file_path)
            moved_files.append(file_path2)
        else:
            os.remove(file_path2)
            moved_files.append(file_path2 + " (deleted duplicate)")
    return moved_files

def log_actions(log_file, moved_files):
    """Log moved and deleted files."""
    with open(log_file, 'w',encoding='utf-8') as f:
        for file in moved_files:
            f.write(file + '\n')
            print(file)

def main():
    folder1 = input("The path to folder 1")
    folder2 = input("The path to folder 2")
    fol_name="The common"
    f_name="dublicate_remove.txt"
    dump_path = "E:/sync/Projects/Git/ZZZ/Dump/"
    log_path ="E:/sync/Projects/Git/ZZZ/log/"
    common_folder = dump_path+fol_name
    log_file = log_path+f_name

    common_hashes, folder1_files, folder2_files = find_common_files(folder1, folder2)
    moved_files = move_common_files(common_hashes, folder1_files, folder2_files, common_folder)
    log_actions(log_file, moved_files)

if __name__ == "__main__":
    main()
