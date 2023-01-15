import os
import re
import py_conv
import c_conv

REPO = os.getcwd() + "\\repo"
NEW_REPO = os.getcwd() + "\\new_repo"

FOLDERS = []

def find_folder(path: str):
    for object in os.listdir(path):
        if not os.path.isfile(path + "\\" + object):
            FOLDERS.append(object)

def create_folder(path: str):
    for object in FOLDERS:
        if not os.path.isdir(path + "\\" + object):
            os.makedirs(path + "\\" + object)

def convert_to_html(path: str, path_to_post: str):
    for object in os.listdir(path):
        abs_path = path + "\\" + object
        if os.path.isfile(abs_path):
            if re.search(r'.py$', object):
                py_conv.python_converter(abs_path, path_to_post + "\\" + re.sub(r'.py$', '.py.html', object))
            if re.search(r'.cpp$', object):
                c_conv.c_converter(abs_path, path_to_post + "\\" + re.sub(r'.cpp$', '.cpp.html', object))
            if re.search(r'.h$', object):
                c_conv.c_converter(abs_path, path_to_post + "\\" + re.sub(r'.h$', '.h.html', object))
        else: convert_to_html(abs_path, path_to_post)

def main():
    find_folder(REPO)
    create_folder(NEW_REPO)
    for folder in FOLDERS:
        convert_to_html(REPO + "\\" + folder, NEW_REPO + "\\" + folder)

if __name__ == "__main__":
    main()