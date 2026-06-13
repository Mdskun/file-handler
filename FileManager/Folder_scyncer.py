import os
import shutil
import filecmp
import logging

print("This program syncs two folders\n")

# Configure logging
path ="E:/sync/Projects/Git/ZZZ/logs/"
f_name="sync_folders.log"
logging.basicConfig(filename=path+f_name, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def sync_folders(folderA, folderB):
    for dirpath, dirnames, filenames in os.walk(folderA):
        # Calculate the relative path of the current directory from the base folder
        rel_path = os.path.relpath(dirpath, folderA)
        
        # Create corresponding directory in folderB
        target_dir = os.path.join(folderB, rel_path)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
            logging.info(f'Created directory: {target_dir}')

        for filename in filenames:
            fileA = os.path.join(dirpath, filename)
            fileB = os.path.join(target_dir, filename)
            
            if not os.path.exists(fileB):
                shutil.copy2(fileA, fileB)
                logging.info(f'Copied {fileA} to {fileB}')
            elif not filecmp.cmp(fileA, fileB, shallow=False):
                # Files are different, move fileB to correct subfolder in folderB
                correct_subfolder = os.path.join(folderB, rel_path)
                if not os.path.exists(correct_subfolder):
                    os.makedirs(correct_subfolder)
                    logging.info(f'Created directory: {correct_subfolder}')
                
                new_fileB = os.path.join(correct_subfolder, filename)
                shutil.move(fileB, new_fileB)
                logging.info(f'Moved {fileB} to {new_fileB}')

    for dirpath, dirnames, filenames in os.walk(folderB):
        rel_path = os.path.relpath(dirpath, folderB)
        target_dir = os.path.join(folderA, rel_path)

        for filename in filenames:
            fileB = os.path.join(dirpath, filename)
            fileA = os.path.join(target_dir, filename)
            
            if not os.path.exists(fileA):
                shutil.copy2(fileB, fileA)
                logging.info(f'Copied {fileB} to {fileA}')
            elif not filecmp.cmp(fileA, fileB, shallow=False):
                # Files are different, move fileA to correct subfolder in folderA
                correct_subfolder = os.path.join(folderA, rel_path)
                if not os.path.exists(correct_subfolder):
                    os.makedirs(correct_subfolder)
                    logging.info(f'Created directory: {correct_subfolder}')
                
                new_fileA = os.path.join(correct_subfolder, filename)
                shutil.move(fileA, new_fileA)
                logging.info(f'Moved {fileA} to {new_fileA}')

if __name__ == '__main__':
    folderA = input('path/to/folderA')
    folderB = input('path/to/folderB')
    sync_folders(folderA, folderB)
    print('Folders synchronized. Check the log file for details.')
