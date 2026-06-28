import os
from pathlib import Path
import stat
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm

print("🚀 Advanced File Report Generator\n")

# ---------- CONFIG ----------
IGNORE_DIRS = {
    "__pycache__", ".git", ".idea", ".vscode",
    "node_modules", "venv", "env", ".venv",
    "System Volume Information", "$RECYCLE.BIN"
}

TOP_N_LARGEST = 10  # show top 10 largest files


# ---------- HIDDEN CHECK ----------
def is_hidden(path: Path):
    if path.name.startswith('.'):
        return True

    if os.name == 'nt':
        try:
            return bool(os.stat(path).st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN)
        except Exception:
            return False

    return False


# ---------- CLASSIFY ----------
def classify_file(path):
    suffix = path.suffix.lower()

    mapping = {
        "mp3": ['.mp3'],
        "mp4": ['.mp4'],
        "mvi": ['.mvi'],
        "jpg": ['.jpg', '.jpeg'],
        "png": ['.png'],
        "pdf": ['.pdf'],
        "word": ['.doc', '.docx'],
        "power point": ['.ppt', '.pptx'],
        "exel": ['.xls', '.xlsx', '.csv'],
        "zip": ['.zip'],
        "java": ['.java'],
        "txt": ['.txt'],
        "log": ['.log'],
        "html": ['.html'],
        "css": ['.css'],
        "javascript": ['.js'],
        "py": ['.py']
    }

    for key, exts in mapping.items():
        if suffix in exts:
            return key

    return None


# ---------- PROCESS FUNCTION (for multiprocessing) ----------
def process_file(file_path_str):
    path = Path(file_path_str)

    try:
        size = path.stat().st_size
    except:
        size = 0

    file_type = classify_file(path)

    return file_type, size, str(path)


# ---------- MULTIPROCESS FILE REPORT ----------
def file_report_of(path):
    path = Path(path)

    result = {
        "mp3":0,"mp4":0,"mvi":0,"jpg":0,"png":0,"pdf":0,"txt":0,"log":0,
        "word":0,"power point":0,"exel":0,"zip":0,"html":0,"css":0,
        "javascript":0,"py":0,"java":0
    }

    files = []

    print("🔍 Scanning files...")

    for item in path.rglob('*'):
        if is_hidden(item):
            continue

        if any(part in IGNORE_DIRS for part in item.parts):
            continue

        if item.is_file():
            files.append(str(item))

    total_size = 0
    largest_files = []

    print(f"⚡ Processing {len(files)} files...\n")

    with ProcessPoolExecutor() as executor:
        results = list(tqdm(executor.map(process_file, files), total=len(files)))

    for file_type, size, filepath in results:
        total_size += size

        if file_type:
            result[file_type] += 1

        largest_files.append((size, filepath))

    # Get top largest files
    largest_files.sort(reverse=True)
    largest_files = largest_files[:TOP_N_LARGEST]

    return result, total_size, largest_files


# ---------- TREE ----------
def generate_directory_tree(folder_path, file, prefix="", exclude_folders=None):
    folder = Path(folder_path)

    if exclude_folders is None:
        exclude_folders = []

    items = sorted(folder.iterdir(), key=lambda x: x.name.lower())

    filtered = []
    for item in items:
        if is_hidden(item):
            continue

        if item.name in IGNORE_DIRS:
            continue

        if any(item.resolve() == Path(ex).resolve() for ex in exclude_folders):
            continue

        filtered.append(item)

    for i, item in enumerate(filtered):
        is_last = i == len(filtered) - 1
        connector = "└── " if is_last else "├── "

        file.write(f"{prefix}{connector}{item.name}\n")

        if item.is_dir():
            new_prefix = prefix + ("    " if is_last else "│   ")
            generate_directory_tree(item, file, new_prefix, exclude_folders)


# ---------- SIZE FORMAT ----------
def human_readable(size):
    for unit in ['B','KB','MB','GB','TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024


# ---------- SAVE ----------
def save_directory_tree_to_file(folder_path, output_file_path, exclude_folders=None):
    folder_path = Path(folder_path)

    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(f"Directory tree for {folder_path}:\n\n")

        generate_directory_tree(folder_path, file, exclude_folders=exclude_folders)

        report, total_size, largest_files = file_report_of(folder_path)

        file.write("\n\n--------> Summary:\n")

        for key, value in report.items():
            if value > 0:
                file.write(f"\n----> {value} files of type {key}")

        file.write(f"\n\n📦 Total Size: {human_readable(total_size)}\n")

        file.write("\n🔥 Largest Files:\n")
        for size, path in largest_files:
            file.write(f"\n{human_readable(size)}  -->  {path}")


# ---------- MAIN ----------
if __name__ == "__main__":
    path = input("Enter path:\n")
    path = Path(path).resolve()

    exclude_input = input("Exclude folders (comma-separated): ")

    if exclude_input.strip():
        exclude_folders = [path / f.strip() for f in exclude_input.split(",")]
    else:
        exclude_folders = []

    save_path = Path("/home/hp/Data/Dump/")
    save_path.mkdir(parents=True, exist_ok=True)

    output_file = save_path / "File_repo.txt"

    save_directory_tree_to_file(path, output_file, exclude_folders)

    print("\n✅ DONE! Report saved at:", output_file)