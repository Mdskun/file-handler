import os
import zipfile
import logging

print("This folder compares zipfile's files and a folder's files then extract whats not in folder\n")
print("Main purpose was spoti-download and incomplate zip extraction\n")

# Set up logging
path = "E:/sync/Projects/Git/ZZZ/log/"
f_name="extraction_log.log"
logging.basicConfig(filename=path+f_name, level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def get_zip_file_list(zip_file_path):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        return zip_ref.namelist()

def get_extracted_file_list(extracted_dir):
    extracted_files = []
    for root, dirs, files in os.walk(extracted_dir):
        for file in files:
            extracted_files.append(os.path.relpath(os.path.join(root, file), extracted_dir))
    return extracted_files

def extract_missing_files(zip_file_path, extracted_dir, missing_files):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        for file in missing_files:
            try:
                zip_ref.extract(file, extracted_dir)
                logging.info(f'Successfully extracted {file}')
            except Exception as e:
                logging.error(f'Failed to extract {file}: {e}')

def main(zip_file_path, extracted_dir):
    logging.info('Starting comparison between extracted files and zip files.')

    zip_file_list = get_zip_file_list(zip_file_path)
    extracted_file_list = get_extracted_file_list(extracted_dir)

    missing_files = [file for file in zip_file_list if file not in extracted_file_list]

    if missing_files:
        logging.info(f'Found {len(missing_files)} missing files. Starting extraction.')
        extract_missing_files(zip_file_path, extracted_dir, missing_files)
        logging.info('Extraction of missing files completed.')
    else:
        logging.info('No missing files found. All files are already extracted.')

if __name__ == '__main__':
    # Replace these paths with the actual paths
    zip_file_path = input("Enter zip file to see")
    extracted_dir = input('Enter folder to see')
    
    main(zip_file_path, extracted_dir)
