import os
import re

def parse_tree(tree_text: str):
    """
    Parse a 'tree' output into a list of file and folder paths.
    """
    paths = []
    stack = []

    lines = tree_text.strip().splitlines()

    for i, raw_line in enumerate(lines):
        # Remove tree drawing characters (├, └, │, ─)
        line = re.sub(r"[├└│─]", " ", raw_line)

        # Count leading spaces = indent
        indent = len(line) - len(line.lstrip(" "))

        # Extract the actual name
        name = line.strip()

        # Determine current depth (4 spaces ≈ 1 level in `tree`)
        depth = indent // 4

        # Adjust stack
        stack = stack[:depth]
        stack.append(name)

        # Check if this is a folder:
        is_folder = name.endswith("/") or (
            i + 1 < len(lines) and
            (len(re.sub(r"[├└│─]", " ", lines[i+1])) - len(lines[i+1].lstrip(" "))) > indent
        )

        if is_folder:
            paths.append(os.path.join(*stack) + os.sep)
        else:
            paths.append(os.path.join(*stack))

    return paths


def create_structure(paths, base_path="./OutputProject"):
    """
    Create folders and empty files based on parsed paths.
    """
    for path in paths:
        abs_path = os.path.join(base_path, path)

        if path.endswith(os.sep):  # Folder
            os.makedirs(abs_path, exist_ok=True)
        else:  # File
            os.makedirs(os.path.dirname(abs_path), exist_ok=True)
            with open(abs_path, "w", encoding="utf-8") as f:
                f.write("")


if __name__ == "__main__":
    tree_file = os.path.abspath(input("File path which has structure:\n"))
    with open(tree_file, "r", encoding="utf-8") as f:
        tree_string = f.read()

    paths = parse_tree(tree_string)
    create_structure(paths, base_path="./Generated")

    print("✅ Project structure created inside ./Generated")
