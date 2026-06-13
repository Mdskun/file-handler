import os
from docx import Document
from pdf2docx import Converter
import comtypes.client

def docx_to_pdf(input_path, output_path):
    word = comtypes.client.CreateObject('Word.Application')
    word.Visible = False
    doc = word.Documents.Open(os.path.abspath(input_path))
    doc.SaveAs(os.path.abspath(output_path), FileFormat=17)  # 17 is for PDF
    doc.Close()
    word.Quit()
    print(f'Converted {input_path} to {output_path}')

def pdf_to_docx(input_path, output_path):
    cv = Converter(input_path)
    cv.convert(output_path, start=0, end=None)
    cv.close()
    print(f'Converted {input_path} to {output_path}')
