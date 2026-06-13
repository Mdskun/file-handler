import os
import re
import time

print("This program normalizes names of files of a folde\n")

def remove_sqbrack():
    for name in os.listdir(directory):
        file_name=re.sub(r'\[.*?\]','',name)
        if(name!=file_name):
            os.rename(directory+name,directory+file_name)
            print("\n->"+name+"--> to -->"+file_name+" :changed here")
    time.sleep(2)
    print("\n--->Sq brackets deleted")

def remove_brack():
    for name in os.listdir(directory):
        file_name=re.sub(r'\(.*?\)','',name)
        if(name!=file_name):
            os.rename(directory+name,directory+file_name)
            print("\n->"+name+"--> to -->"+file_name+" :changed here")
    time.sleep(2)
    print("\n--->norm brackets deleted")

def remove_2space():
    for name in os.listdir(directory):
        file_name=re.sub(r'  ',' ',name)
        file_name=re.sub(r' \.mp3','.mp3',file_name)
        if(name!=file_name):
            os.rename(directory+name,directory+file_name)
            print("\n->"+name+"--> to -->"+file_name+" :changed here")
    time.sleep(2)
    print("\n--->space deleted")

def remove_words():
    for name in os.listdir(directory):
        file_name=re.sub(r'[-_]',' ',name)
        file_name=re.sub(r'\,',' ',file_name)
        file_name=re.sub(r'\.\.',' ',file_name)
        file_name=re.sub(r'Official','',file_name)
        file_name=re.sub(r'official','',file_name)
        file_name=re.sub(r'bgm','',file_name)
        file_name=re.sub(r'Bgm','',file_name)
        file_name=re.sub(r'BGM','',file_name)
        file_name=re.sub(r'Theme','',file_name)
        file_name=re.sub(r'theme','',file_name)
        file_name=re.sub(r'song','',file_name)
        file_name=re.sub(r'Song','',file_name)
        file_name=re.sub(r'Full','',file_name)
        file_name=re.sub(r'full','',file_name)
        file_name=re.sub(r'Music','',file_name)
        file_name=re.sub(r'music','',file_name)
        file_name=re.sub(r'Video','',file_name)
        file_name=re.sub(r'video','',file_name)
        if(name!=file_name):
            os.rename(directory+name,directory+file_name)
        print("\n->"+name+"--> to -->"+file_name+" :changed here")        
    time.sleep(2)
    print("\n--->full,video,music Words deleted")

def remove_kbps():
    for name in os.listdir(directory):
        file_name=re.sub(r'\( ...kbps \)','',name)
        file_name=re.sub(r'...kbps','',file_name)
        file_name=re.sub(r'\( ...Kbps \)','',file_name)
        file_name=re.sub(r'...Kbps','',file_name)
        if(name!=file_name):
            os.rename(directory+name,directory+file_name)
            print("\n->"+name+"--> to -->"+file_name+" :changed here")        
    time.sleep(2)
    print("\n--->all kbps deleted")
    remove_2space()

def all_no_report():
    remove_kbps()
    time.sleep(3)
    remove_sqbrack()
    time.sleep(3)
    remove_brack()
    time.sleep(3)
    remove_words()
    time.sleep(3)
    remove_2space()

#all_no_report()

def name_file():
    with open("names.txt",'a') as file:
        file.write("\n------>"+directory+"<------")
        for name in os.listdir(directory):
            file.write("\n"+name)
    print("done!!!!")

def remove_some_words():
    for name in os.listdir(directory):
        file_name=re.sub(r' ','',name)
        if(name!=file_name):
            os.rename(directory+name,directory+file_name)
            print("\n->"+name+"--> to -->"+file_name+" :changed here")
    time.sleep(2)
    print("\n--->words deleted")

# name_file()
# time.sleep(3)
# remove_some_words()#it need more modification

if __name__ == "__main__":
    directory=input("Enter directory to change names of it's sub files")
    directory=os.path.abspath(directory)+"/"
    all_no_report()
    print("The names are normalized")