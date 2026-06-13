import os
import re
import shutil
import Word_to_Pdf as converter
Delete=True
path=os.path.abspath(input("\nEnter path:-\n"))
for file in os.listdir(path):
    if file.endswith("pdf"):
        print("\nstarting....")
        tname=re.sub(r'\.pdf','',file)
        converter.pdf_to_docx(path+"\\"+file,path+"\\"+tname+".docx")
        print("Converted")
        if Delete:
            if not("pdf_moved" in os.listdir(path)):
                os.mkdir(path+"\\"+"pdf_moved")
                print("directory made")
            shutil.move(path+"\\"+file,path+"\\"+"pdf_moved"+"\\"+file)
            print("File moved")
            
    if file.endswith("docx"):
        tname=re.sub(r'\.docx','',file)
        converter.docx_to_pdf(path+"\\"+file,path+"\\"+tname+".pdf")
        if Delete:
            if not("doc_moved" in os.listdir(path)):
                os.mkdir(path+"\\"+"doc_moved")
            shutil.move(path+"\\"+file,path+"\\"+"doc_moved"+"\\"+file)