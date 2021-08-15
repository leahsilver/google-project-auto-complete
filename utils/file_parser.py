import os


def get_all_files(root: str) -> str:
    count = 0
    for subdir, dirs, files in os.walk(root):
        for file in files:
            count += 1
            yield os.path.join(subdir, file)


def get_all_lines(root: str):
    for file in get_all_files(root):
        i = 0
        with open(file, 'r', encoding="utf8") as file_to_read:
            for line in file_to_read:
                if len(line):
                    yield {"path": file, "line_num": i, "line": line.strip()}
                i += 1
