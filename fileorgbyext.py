import os
import shutil

warning=False
path=os.path.abspath(input("\nEnter directory to organize by extentions:"))

try:
    for file in os.listdir(path):
        if os.path.isdir(path+"/"+file):
            print("\nthis program is made to arrange files only\nNOt touching folder:"+file)
            warning=True
            
        elif file.endswith(('.jpg','.jpeg','.png')):
            if not(os.path.exists(path+"/image")):
                os.mkdir(path+'/image')
            shutil.move(path+"/"+file,path+"/image/"+file)
            print("\nmoved mage file named "+file)
        
        elif file.endswith(('.log')):
            if not(os.path.exists(path+"/log")):
                os.mkdir(path+'/log')
            shutil.move(path+"/"+file,path+"/log/"+file)

        elif file.endswith(('.mvi','.mp3')):
            if not(os.path.exists(path+"/audio")):
                os.mkdir(path+'/audio')
            shutil.move(path+"/"+file,path+"/audio/"+file)

        elif file.endswith(('.zip')):
            if not(os.path.exists(path+"/zip")):
                os.mkdir(path+'/zip')
            shutil.move(path+"/"+file,path+"/zip/"+file)
except Exception as e:
    print(e)

if warning:
    print("Multiple folders detected\nchances to confuse folders increased")