import os
import re

import markdown2
import pdfkit

# Path to wkhtmltopdf (change this to your actual path)
WKHTMLTOPDF_PATH = r"E:\sync\Projects\components\wkhtmltox\bin\wkhtmltopdf.exe"  # Update for your system

# Configure pdfkit
config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)

# HTML/CSS template, with a bit of styling for <code> blocks
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 18px;
            text-align: left;
        }}
        th, td {{
            padding: 8px;
            border: 1px solid black;
        }}
        th {{
            background-color: #f2f2f2;
        }}

        /* Styling for code blocks */
        pre {{
            background-color: #f8f8f8;
            padding: 10px;
            border: 1px solid #ddd;
            overflow-x: auto;
        }}
        code {{
            font-family: Consolas, "Courier New", monospace;
        }}
    </style>
</head>
<body>
    {content}
</body>
</html>
"""

def convert_md_to_pdf(md_file, pdf_file):
    # Read Markdown content
    with open(md_file, "r", encoding="utf-8") as f:
        md_content = f.read()
    
    # Convert Markdown to HTML, escaping any raw HTML tags
    html_content = markdown2.markdown(
        md_content,
        extras=[
            "tables",              # keep table support
            "fenced-code-blocks",  # recognize ``` blocks
            "code-friendly"        # make it easier to nest code
        ],
        safe_mode="escape"         # escape any HTML tags so they appear as code
    )
    
    # Wrap the HTML in our template
    full_html = HTML_TEMPLATE.format(content=html_content)
    
    # Generate PDF
    pdfkit.from_string(full_html, pdf_file, configuration=config)
    print(f"Converted {md_file} → {pdf_file}")

if __name__ == "__main__":
    path_for_file = os.path.abspath(input("Enter path to MD file: ").strip())
    # Automatically replace .md with .pdf
    fname = re.sub(r"\.md$", ".pdf", path_for_file, flags=re.IGNORECASE)
    
    print(f"Input MD: {path_for_file}\nOutput PDF: {fname}")
    convert_md_to_pdf(path_for_file, fname)
    os.startfile(fname)
    flag = input("Press T to delete the original .md file: ").strip()
    if flag.upper() == "T":
        os.remove(path_for_file)
