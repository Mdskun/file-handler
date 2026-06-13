import os
import zipfile
import hashlib
import logging

print("This folder compares zipfile's files and deletes dublicates\n")
print("Main purpose was spoti-download\n")

def setup_logging():
    """Set up the logging configuration."""
    path = "E:/sync/Projects/Git/ZZZ/log/"
    f_name="zip_deduplication.log"
    logging.basicConfig(filename=path+f_name,
                        level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

def get_file_hash(file_data):
    """Calculate the MD5 hash of a file's data."""
    hasher = hashlib.md5()
    hasher.update(file_data)
    return hasher.hexdigest()

def scan_zip_files(folder_path):
    """Scan all zip files in the given folder and remove duplicate files."""
    zip_files = [f for f in os.listdir(folder_path) if f.endswith('.zip')]
    
    if len(zip_files) <= 1:
        logging.info("Not enough ZIP files to compare.")
        return

    file_hash_map = {}

    for zip_file in zip_files:
        zip_path = os.path.join(folder_path, zip_file)
        temp_zip_path = zip_path + '.temp'

        with zipfile.ZipFile(zip_path, 'r') as zf:
            file_names = zf.namelist()

            duplicate_found = False

            with zipfile.ZipFile(temp_zip_path, 'w') as temp_zip:
                for file_name in file_names:
                    with zf.open(file_name) as file:
                        file_data = file.read()
                        file_hash = get_file_hash(file_data)

                        if file_hash in file_hash_map:
                            original_zip, original_file = file_hash_map[file_hash]
                            logging.info(f"Duplicate found: '{file_name}' in '{zip_file}' is a duplicate of '{original_file}' in '{original_zip}'")
                            duplicate_found = True
                        else:
                            file_hash_map[file_hash] = (zip_file, file_name)
                            temp_zip.writestr(file_name, file_data)

            if duplicate_found:
                # Close all references and replace the original zip with the temp one
                zf.close()
                os.remove(zip_path)
                os.rename(temp_zip_path, zip_path)
                logging.info(f"Updated '{zip_file}' by removing duplicates.")
            else:
                # No duplicates found, remove the temp file
                os.remove(temp_zip_path)

if __name__ == "__main__":
    setup_logging()
    folder_path = input("Give folder path to find zip dublicates")  # Replace with your folder path
    scan_zip_files(folder_path)
