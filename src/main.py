source = "static"
from os import listdir, mkdir
from os.path import join, abspath, dirname, exists, isfile
from shutil import copy, rmtree

# directory where this script lives
script_dir = dirname(abspath(__file__))
public = join(script_dir, "..", "public")
static = join(script_dir, "..", "static")


def copy_folder(static_path: str, public_path: str):
    static_map = listdir(static_path)
    if not exists(public_path):
        mkdir(public_path)

    for file in static_map:
        file_src = join(static_path, file)
        file_dest = join(public_path, file)
        if isfile(file_src):
            copy(file_src, file_dest)
        else:
            copy_folder(file_src, file_dest)


def cp_data():
    if exists(public) and not isfile(public):
        rmtree(public)

    if not exists(public):
        mkdir(public)

    if exists(static) and not isfile(static):
        copy_folder(static, public)


def main():
    cp_data()


if __name__ == "__main__":
    main()
