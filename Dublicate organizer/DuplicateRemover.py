import os
import hashlib

print("This program deletes dublicates from one folder\n")

def calculate_file_hash(file_path, hash_algo=hashlib.sha256):
    """Calculate the hash of a file."""
    hash_obj = hash_algo()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hash_obj.update(chunk)
    return hash_obj.hexdigest()

def find_and_remove_duplicates(directory):
    """Find and remove duplicate files in a directory."""
    hash_map = {}  # Stores file hash to file path mapping
    duplicates = []  # Stores paths of duplicate files

    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_hash = calculate_file_hash(file_path)
            
            if file_hash in hash_map:
                duplicates.append(file_path)
            else:
                hash_map[file_hash] = file_path

    # Log duplicates
    log_path ="E:/sync/Projects/Git/ZZZ/logs/"
    f_name="duplicates_log.log"
    with open(log_path+f_name, "w") as log_file:
        for dup in duplicates:
            log_file.write(f"Duplicate file: {dup}\n")
    
    # Remove duplicates
    for dup in duplicates:
        os.remove(dup)
        print(f"Deleted duplicate file: {dup}")

if __name__ == "__main__":
    directory_to_clean = input("Enter the directory path to search for duplicates: ")
    find_and_remove_duplicates(directory_to_clean)
    print("Duplicate file search and removal complete. Check 'duplicates_log.log' for details.")