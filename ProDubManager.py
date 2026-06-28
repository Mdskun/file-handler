import os
import hashlib
import shutil
import json
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor

print("\nUltra Fast Duplicate Manager\n")

# ---------------- SETTINGS ---------------- #
MOVE_DUPLICATES = True
DELETE_DUPLICATES = False
KEEP_NEWEST = True

DUPLICATE_FOLDER_NAME = "Duplicates"
LOG_FILE = "duplicate_log.txt"
CACHE_FILE = "hash_cache.json"

PARTIAL_HASH_SIZE = 4096
SAMPLE_OFFSET = 1024 * 1024  # 1MB offset sample
MAX_WORKERS = os.cpu_count()

FILE_EXTENSIONS = None  # e.g. ('.mp3', '.jpg')
# ------------------------------------------ #

# ---------- HASHING ---------- #

def get_file_info(path):
    return (path, os.path.getsize(path), os.path.getmtime(path))

def partial_hash(path):
    try:
        with open(path, 'rb') as f:
            return hashlib.md5(f.read(PARTIAL_HASH_SIZE)).hexdigest()
    except:
        return None

def sample_hash(path):
    try:
        with open(path, 'rb') as f:
            f.seek(SAMPLE_OFFSET)
            return hashlib.md5(f.read(PARTIAL_HASH_SIZE)).hexdigest()
    except:
        return None

def full_hash(path):
    try:
        hasher = hashlib.sha256()
        with open(path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                hasher.update(chunk)
        return hasher.hexdigest()
    except:
        return None

# ---------- CACHE ---------- #

def load_cache(base_folder):
    path = os.path.join(base_folder, CACHE_FILE)
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    return {}

def save_cache(cache, base_folder):
    path = os.path.join(base_folder, CACHE_FILE)
    with open(path, 'w') as f:
        json.dump(cache, f)

# ---------- CORE ---------- #

def collect_files(folders):
    files = []
    for folder in folders:
        for root, _, filenames in os.walk(folder):
            for name in filenames:
                if FILE_EXTENSIONS and not name.lower().endswith(FILE_EXTENSIONS):
                    continue
                files.append(os.path.join(root, name))
    return files

def group_by_size(files):
    size_map = defaultdict(list)
    for f in files:
        try:
            size_map[os.path.getsize(f)].append(f)
        except:
            pass
    return size_map

def parallel_hash(files, func):
    with ProcessPoolExecutor(MAX_WORKERS) as executor:
        results = list(executor.map(func, files))
    return dict(zip(files, results))

def find_duplicates(files, cache):
    size_map = group_by_size(files)
    duplicates = []

    for size, group in size_map.items():
        if len(group) < 2:
            continue

        print(f"\nProcessing size group: {size} ({len(group)} files)")

        # Partial hash
        p_hashes = parallel_hash(group, partial_hash)
        p_map = defaultdict(list)
        for f, h in p_hashes.items():
            if h:
                p_map[h].append(f)

        for p_group in p_map.values():
            if len(p_group) < 2:
                continue

            # Sample hash
            s_hashes = parallel_hash(p_group, sample_hash)
            s_map = defaultdict(list)
            for f, h in s_hashes.items():
                if h:
                    s_map[h].append(f)

            for s_group in s_map.values():
                if len(s_group) < 2:
                    continue

                # Full hash (with cache)
                full_map = defaultdict(list)

                for f in s_group:
                    key = f"{f}:{os.path.getmtime(f)}"

                    if key in cache:
                        h = cache[key]
                    else:
                        h = full_hash(f)
                        cache[key] = h

                    if h:
                        full_map[h].append(f)

                for group in full_map.values():
                    if len(group) > 1:
                        duplicates.append(group)

    return duplicates

# ---------- ACTION ---------- #

def pick_keep(files):
    return max(files, key=os.path.getmtime) if KEEP_NEWEST else files[0]

def handle_duplicates(duplicates, base_folder):
    dup_folder = os.path.join(base_folder, DUPLICATE_FOLDER_NAME)
    os.makedirs(dup_folder, exist_ok=True)

    logs = []

    for group in duplicates:
        keep = pick_keep(group)

        for f in group:
            if f == keep:
                continue

            try:
                if MOVE_DUPLICATES:
                    target = os.path.join(dup_folder, os.path.basename(f))

                    counter = 1
                    while os.path.exists(target):
                        name, ext = os.path.splitext(target)
                        target = f"{name}_{counter}{ext}"
                        counter += 1

                    shutil.move(f, target)
                    logs.append(f"MOVED: {f} -> {target}")

                elif DELETE_DUPLICATES:
                    os.remove(f)
                    logs.append(f"DELETED: {f}")

            except Exception as e:
                logs.append(f"ERROR: {f} ({e})")

    return logs

def save_log(logs, base_folder):
    path = os.path.join(base_folder, LOG_FILE)
    with open(path, 'w', encoding='utf-8') as f:
        for l in logs:
            f.write(l + "\n")
            print(l)

# ---------- MAIN ---------- #

def main():
    paths = input("Enter folders (comma separated): ").split(",")
    folders = [p.strip() for p in paths if os.path.exists(p.strip())]

    if not folders:
        print("Invalid paths")
        return

    base = folders[0]

    print("\nLoading cache...")
    cache = load_cache(base)

    print("Scanning files...")
    files = collect_files(folders)
    print(f"Total files: {len(files)}")

    print("\nFinding duplicates...")
    duplicates = find_duplicates(files, cache)

    print(f"\nDuplicate groups: {len(duplicates)}")

    if duplicates:
        logs = handle_duplicates(duplicates, base)
        save_log(logs, base)

    print("\nSaving cache...")
    save_cache(cache, base)

    print("\nDone.")

if __name__ == "__main__":
    main()