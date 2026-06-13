import csv
import json

# Extract CSV formatting
def extract_csv_formatting(file_path,json_file_path):
    with open(file_path, mode='r', newline='') as csvfile:
        sample = csvfile.read(1024)  # Read a sample of the file
        sniffer = csv.Sniffer()
        dialect = sniffer.sniff(sample)
        formatting = {
            "delimiter": dialect.delimiter,
            "quotechar": dialect.quotechar,
            "quoting": dialect.quoting,
            "escapechar": dialect.escapechar,
            "lineterminator": dialect.lineterminator,
            "skipinitialspace": dialect.skipinitialspace,
            "doublequote": dialect.doublequote,
            "dialect_name": dialect.__class__.__name__,
        }
    with open(json_file_path, mode='w') as json_file:
        json.dump(formatting, json_file, indent=4)

# Apply formatting to another CSV
def apply_formatting_to_csv(source_file, target_file, formatting_json):
    with open(formatting_json, mode='r') as json_file:
        formatting = json.load(json_file)

    with open(source_file, mode='r', newline='') as infile, \
         open(target_file, mode='w', newline=formatting["lineterminator"]) as outfile:
        
        reader = csv.reader(
            infile,
            delimiter=formatting["delimiter"],
            quotechar=formatting["quotechar"],
            quoting=formatting["quoting"],
            escapechar=formatting["escapechar"],
            skipinitialspace=formatting["skipinitialspace"],
            doublequote=formatting["doublequote"]
        )
        writer = csv.writer(
            outfile,
            delimiter=formatting["delimiter"],
            quotechar=formatting["quotechar"],
            quoting=formatting["quoting"],
            escapechar=formatting["escapechar"],
            skipinitialspace=formatting["skipinitialspace"],
            doublequote=formatting["doublequote"],
            lineterminator=formatting["lineterminator"]
        )
        writer.writerows(reader)

# Example Usage
source_csv = r"E:\csv\nov 24\ABAD_919426.csv"
target_csv = "target.csv"
formatting_json = "formatting2.json"

# Extract and save formatting
extract_csv_formatting(source_csv,formatting_json)

# Apply formatting
# apply_formatting_to_csv("another_source.csv", target_csv, formatting_json)
""" change this "import csv
import json

# Extract CSV formatting
def extract_csv_formatting(file_path,json_file_path):
    with open(file_path, mode='r', newline='') as csvfile:
        sample = csvfile.read(1024)  # Read a sample of the file
        sniffer = csv.Sniffer()
        dialect = sniffer.sniff(sample)
        formatting = {
            "delimiter": dialect.delimiter,
            "quotechar": dialect.quotechar,
            "quoting": dialect.quoting,
            "escapechar": dialect.escapechar,
            "lineterminator": dialect.lineterminator,
            "skipinitialspace": dialect.skipinitialspace,
            "doublequote": dialect.doublequote,
            "dialect_name": dialect.__class__.__name__,
        }
    with open(json_file_path, mode='w') as json_file:
        json.dump(formatting, json_file, indent=4)

# Apply formatting to another CSV
def apply_formatting_to_csv(source_file, target_file, formatting_json):
    with open(formatting_json, mode='r') as json_file:
        formatting = json.load(json_file)

    with open(source_file, mode='r', newline='') as infile, \
         open(target_file, mode='w', newline=formatting["lineterminator"]) as outfile:
        
        reader = csv.reader(
            infile,
            delimiter=formatting["delimiter"],
            quotechar=formatting["quotechar"],
            quoting=formatting["quoting"],
            escapechar=formatting["escapechar"],
            skipinitialspace=formatting["skipinitialspace"],
            doublequote=formatting["doublequote"]
        )
        writer = csv.writer(
            outfile,
            delimiter=formatting["delimiter"],
            quotechar=formatting["quotechar"],
            quoting=formatting["quoting"],
            escapechar=formatting["escapechar"],
            skipinitialspace=formatting["skipinitialspace"],
            doublequote=formatting["doublequote"],
            lineterminator=formatting["lineterminator"]
        )
        writer.writerows(reader)

# Example Usage
source_csv = r"E:\csv\nov 24\ABAD_919426.csv"
target_csv = "target.csv"
formatting_json = "formatting2.json"

# Extract and save formatting
extract_csv_formatting(source_csv,formatting_json)

# Apply formatting
# apply_formatting_to_csv("another_source.csv", target_csv, formatting_json)
" script so that it can also detect things """